"""Small helpers for portfolio content syncing."""
from __future__ import annotations

import re
from dataclasses import dataclass
from html import unescape
from html.parser import HTMLParser
from typing import Optional
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


@dataclass
class LinkPreview:
    title: str = ""
    description: str = ""
    image_url: str = ""
    site_name: str = ""
    platform: str = "blog"


class MetadataParser(HTMLParser):
    """Extract OpenGraph, Twitter card, title and meta description."""

    def __init__(self) -> None:
        super().__init__()
        self.meta: dict[str, str] = {}
        self.title_parts: list[str] = []
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, Optional[str]]]) -> None:
        attrs_dict = {key.lower(): (value or "") for key, value in attrs}
        if tag.lower() == "title":
            self._in_title = True
            return
        if tag.lower() != "meta":
            return

        key = attrs_dict.get("property") or attrs_dict.get("name") or attrs_dict.get("itemprop")
        content = attrs_dict.get("content")
        if key and content:
            self.meta[key.lower()] = unescape(content).strip()

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self._in_title = False

    @property
    def page_title(self) -> str:
        return " ".join(part.strip() for part in self.title_parts if part.strip())


def detect_platform(url: str) -> str:
    host = urlparse(url).netloc.lower()
    if "linkedin.com" in host:
        return "linkedin"
    if "medium.com" in host:
        return "medium"
    if "dev.to" in host:
        return "devto"
    if "hashnode" in host:
        return "hashnode"
    return "blog"


def clean_text(value: str, max_length: int = 500) -> str:
    value = re.sub(r"\s+", " ", value or "").strip()
    return value[:max_length].rstrip()


def fetch_link_preview(url: str, timeout: int = 10) -> LinkPreview:
    """
    Fetch metadata for blog/LinkedIn links.

    LinkedIn sometimes blocks anonymous scraping. In that case this returns a
    safe fallback using the URL host so the owner can still save the link and
    manually edit title/description if needed.
    """
    platform = detect_platform(url)
    host = urlparse(url).netloc.replace("www.", "")
    fallback = LinkPreview(title=host or url, site_name=host, platform=platform)

    try:
        request = Request(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "KHTML, like Gecko) Chrome/124.0 Safari/537.36"
                ),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            },
        )
        with urlopen(request, timeout=timeout) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            html = response.read(1_000_000).decode(charset, errors="replace")
    except (HTTPError, URLError, TimeoutError, ValueError):
        return fallback

    parser = MetadataParser()
    parser.feed(html)
    meta = parser.meta

    title = clean_text(
        meta.get("og:title")
        or meta.get("twitter:title")
        or parser.page_title
        or fallback.title,
        250,
    )
    description = clean_text(
        meta.get("og:description")
        or meta.get("twitter:description")
        or meta.get("description")
        or "",
        500,
    )
    image_url = clean_text(
        meta.get("og:image")
        or meta.get("twitter:image")
        or meta.get("twitter:image:src")
        or "",
        500,
    )
    site_name = clean_text(meta.get("og:site_name") or host, 120)

    return LinkPreview(
        title=title,
        description=description,
        image_url=image_url,
        site_name=site_name,
        platform=platform,
    )


@dataclass
class GitCommitPreview:
    message: str = ""
    commit_hash: str = ""
    committed_at: str = ""


def parse_github_repo(url: str) -> tuple[str, str] | None:
    parsed = urlparse(url or "")
    if "github.com" not in parsed.netloc.lower():
        return None
    parts = [part for part in parsed.path.strip("/").split("/") if part]
    if len(parts) < 2:
        return None
    repo = parts[1].removesuffix(".git")
    return parts[0], repo


def fetch_github_latest_commit(repo_url: str, timeout: int = 10) -> GitCommitPreview | None:
    """Fetch the latest commit for a public GitHub repository URL."""
    repo = parse_github_repo(repo_url)
    if not repo:
        return None
    owner, name = repo
    api_url = f"https://api.github.com/repos/{owner}/{name}/commits?per_page=1"
    try:
        request = Request(
            api_url,
            headers={
                "User-Agent": "Django-Portfolio-Commit-Sync",
                "Accept": "application/vnd.github+json",
            },
        )
        with urlopen(request, timeout=timeout) as response:
            payload = response.read(500_000).decode("utf-8", errors="replace")
    except (HTTPError, URLError, TimeoutError, ValueError):
        return None

    import json

    try:
        data = json.loads(payload)
        item = data[0]
        commit = item.get("commit", {})
        return GitCommitPreview(
            message=clean_text(commit.get("message", "").split("\n", 1)[0], 255),
            commit_hash=clean_text(item.get("sha", "")[:12], 80),
            committed_at=clean_text(commit.get("committer", {}).get("date", ""), 80),
        )
    except (KeyError, IndexError, TypeError, ValueError):
        return None
