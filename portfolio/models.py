from __future__ import annotations

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class SiteProfile(models.Model):
    """Single editable owner/profile record used by the public site and dashboard."""

    name = models.CharField(max_length=120, default="Afzal Khan")
    logo_text = models.CharField(max_length=12, default="AK")
    title = models.CharField(max_length=160, default="Senior Odoo Developer & ERP Consultant")
    role_highlight = models.CharField(max_length=80, default="Odoo")
    hero_badge = models.CharField(max_length=160, default="Available for ERP consulting and Odoo implementation projects")
    bio = models.TextField(
        default=(
            "I design and develop reliable Odoo ERP solutions for companies that need cleaner workflows, "
            "stronger automation and practical business reporting."
        )
    )
    about_long = models.TextField(
        default=(
            "I specialize in Odoo ERP customization, Django backend development, reporting, integrations "
            "and workflow automation. My work focuses on practical business value: clean data structures, "
            "responsive interfaces, maintainable code and systems that teams can use confidently every day."
        )
    )
    email = models.EmailField(default="afzalkhan101@gmail.com")
    github = models.URLField(blank=True, default="https://github.com/afzalkhan101")
    linkedin = models.URLField(blank=True, default="https://www.linkedin.com/")
    twitter = models.CharField(max_length=255, blank=True, default="#")
    youtube = models.CharField(max_length=255, blank=True, default="#")
    profile_picture = models.FileField(upload_to="profile/", blank=True)
    stats_text = models.TextField(
        default="6+ | Years Experience | ▰\n40+ | Modules Built | ✦\n20+ | Happy Clients | ↗",
        help_text="One stat per line: value | label | icon",
    )
    services_text = models.TextField(
        default="Custom Module Development\nOdoo Implementation\nOdoo Integration\nPerformance Optimization",
        help_text="One service per line.",
    )
    focus_areas_text = models.TextField(
        default=(
            "⚙️ | Odoo ERP | Custom modules, reports, approval workflows and business automation.\n"
            "🐍 | Django Backend | Database-driven apps, dashboards, forms and clean admin tools.\n"
            "📊 | Business Systems | Accounting, sales, inventory and operations-focused workflows."
        ),
        help_text="One focus area per line: icon | label | description",
    )
    skills_text = models.TextField(
        default="Odoo, Python, Django, PostgreSQL, JavaScript, Tailwind CSS, Docker, Nginx",
        help_text="Comma or line separated skills.",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Profile"
        verbose_name_plural = "Site Profile"

    def __str__(self) -> str:
        return self.name

    @classmethod
    def load(cls) -> "SiteProfile":
        profile, _created = cls.objects.get_or_create(pk=1)
        return profile

    def _line_items(self, text: str) -> list[str]:
        return [line.strip() for line in (text or "").splitlines() if line.strip()]

    @property
    def stats(self) -> list[dict[str, str]]:
        items: list[dict[str, str]] = []
        for line in self._line_items(self.stats_text):
            value, label, icon = (part.strip() for part in (line.split("|") + ["", "", ""])[:3])
            if value and label:
                items.append({"value": value, "label": label, "icon": icon or "✦"})
        return items

    @property
    def services(self) -> list[str]:
        return self._line_items(self.services_text)

    @property
    def focus_areas(self) -> list[dict[str, str]]:
        items: list[dict[str, str]] = []
        for line in self._line_items(self.focus_areas_text):
            icon, label, desc = (part.strip() for part in (line.split("|") + ["", "", ""])[:3])
            if label:
                items.append({"icon": icon or "✦", "label": label, "desc": desc})
        return items

    @property
    def skills(self) -> list[str]:
        raw = (self.skills_text or "").replace("\n", ",")
        return [skill.strip() for skill in raw.split(",") if skill.strip()]

    @property
    def profile_image_url(self) -> str:
        if not self.profile_picture:
            return ""
        try:
            return self.profile_picture.url
        except ValueError:
            return ""

    @property
    def title_parts(self) -> dict[str, str]:
        title = self.title.strip()
        highlight = self.role_highlight.strip()
        if not title:
            return {"title_before": "", "title_highlight": "", "title_after": ""}
        if not highlight or highlight.lower() not in title.lower():
            return {"title_before": title, "title_highlight": "", "title_after": ""}
        start = title.lower().find(highlight.lower())
        end = start + len(highlight)
        return {
            "title_before": title[:start].strip(),
            "title_highlight": title[start:end].strip(),
            "title_after": title[end:].strip(),
        }

    def as_context(self) -> dict:
        context = {
            "profile": self,
            "name": self.name,
            "logo_text": self.logo_text,
            "title": self.title,
            "role_highlight": self.role_highlight,
            "hero_badge": self.hero_badge,
            "bio": self.bio,
            "about_long": self.about_long,
            "email": self.email,
            "github": self.github,
            "linkedin": self.linkedin,
            "twitter": self.twitter,
            "youtube": self.youtube,
            "stats": self.stats,
            "services": self.services,
            "focus_areas": self.focus_areas,
            "skills": self.skills,
            "profile_image_url": self.profile_image_url,
        }
        context.update(self.title_parts)
        return context


class Project(models.Model):
    STATUS_CHOICES = [
        ("planning", "Planning"),
        ("active", "Active"),
        ("paused", "Paused"),
        ("completed", "Completed"),
        ("archived", "Archived"),
    ]

    name = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    short_desc = models.CharField("Short description", max_length=240)
    detailed_description = models.TextField(blank=True)
    project_type = models.CharField(max_length=120, blank=True, help_text="Example: Odoo Module, Django App, SaaS")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    tech_stack = models.CharField(max_length=400, blank=True, help_text="Comma separated: Odoo, Python, PostgreSQL")
    repo_url = models.URLField("GitHub / repository URL", blank=True)
    live_url = models.URLField(blank=True)
    image_url = models.URLField(blank=True)
    last_commit_message = models.CharField(max_length=255, blank=True)
    last_commit_hash = models.CharField(max_length=80, blank=True)
    last_commit_at = models.DateTimeField(null=True, blank=True)
    is_featured = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "-last_commit_at", "-updated_at"]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name) or "project"
            slug = base_slug
            counter = 1
            while Project.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f"{base_slug}-{counter}"
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("project_detail", kwargs={"slug": self.slug})

    @property
    def tag_list(self) -> list[str]:
        return [tag.strip() for tag in self.tech_stack.split(",") if tag.strip()]

    def sync_latest_commit(self) -> bool:
        """Update last commit fields from a public GitHub repository URL."""
        if not self.repo_url:
            return False
        from django.utils.dateparse import parse_datetime
        from .services import fetch_github_latest_commit

        preview = fetch_github_latest_commit(self.repo_url)
        if not preview:
            return False
        if preview.message:
            self.last_commit_message = preview.message
        if preview.commit_hash:
            self.last_commit_hash = preview.commit_hash
        if preview.committed_at:
            parsed = parse_datetime(preview.committed_at)
            if parsed:
                self.last_commit_at = parsed
        self.save(update_fields=["last_commit_message", "last_commit_hash", "last_commit_at", "updated_at"])
        return True

    @property
    def feature_count(self) -> int:
        return self.features.count()


class ProjectFeature(models.Model):
    STATUS_CHOICES = [
        ("todo", "Todo"),
        ("progress", "In Progress"),
        ("done", "Done"),
        ("future", "Future"),
    ]

    project = models.ForeignKey(Project, related_name="features", on_delete=models.CASCADE)
    title = models.CharField(max_length=180)
    details = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="done")
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self) -> str:
        return f"{self.project.name}: {self.title}"


class ExternalPost(models.Model):
    PLATFORM_CHOICES = [
        ("blog", "Blog"),
        ("linkedin", "LinkedIn"),
        ("medium", "Medium"),
        ("devto", "Dev.to"),
        ("hashnode", "Hashnode"),
    ]

    url = models.URLField(unique=True)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, default="blog")
    title = models.CharField(max_length=250, blank=True)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    site_name = models.CharField(max_length=120, blank=True)
    is_visible = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    synced_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "-created_at"]

    def __str__(self) -> str:
        return self.title or self.url

    def sync_preview(self, force: bool = False) -> bool:
        """Populate title/description/image/site from the pasted link."""
        if not self.url:
            return False
        if self.title and self.description and self.image_url and not force:
            return False

        from .services import fetch_link_preview

        preview = fetch_link_preview(self.url)
        self.platform = preview.platform or self.platform
        if force or not self.title:
            self.title = preview.title
        if force or not self.description:
            self.description = preview.description
        if force or not self.image_url:
            self.image_url = preview.image_url
        if force or not self.site_name:
            self.site_name = preview.site_name
        self.synced_at = timezone.now()
        return True

    def save(self, *args, **kwargs):
        should_sync = not self.pk or not self.title
        if should_sync:
            self.sync_preview(force=False)
        super().save(*args, **kwargs)
