from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ExternalPostForm, ProjectForm, SiteProfileForm
from .models import ExternalPost, Project, SiteProfile


def base_context() -> dict:
    return SiteProfile.load().as_context()


def home(request):
    context = base_context()
    context.update(
        projects=Project.objects.filter(is_featured=True).prefetch_related("features"),
        posts=ExternalPost.objects.filter(is_visible=True),
    )
    return render(request, "home.html", context)


def project_detail(request, slug):
    project = get_object_or_404(Project.objects.prefetch_related("features"), slug=slug)
    context = base_context()
    context.update(project=project)
    return render(request, "project_detail.html", context)


@login_required
def dashboard(request):
    context = base_context()
    context.update(
        projects=Project.objects.prefetch_related("features"),
        posts=ExternalPost.objects.all(),
    )
    return render(request, "dashboard.html", context)


@login_required
def profile_update(request):
    profile = SiteProfile.load()
    if request.method == "POST":
        form = SiteProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile content updated successfully.")
            return redirect("dashboard")
    else:
        form = SiteProfileForm(instance=profile)
    return render(request, "profile_form.html", {**base_context(), "form": form})


@login_required
def project_create(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            messages.success(request, "Project added successfully.")
            return redirect(project.get_absolute_url())
    else:
        form = ProjectForm()
    return render(request, "project_form.html", {**base_context(), "form": form, "mode": "Create"})


@login_required
def project_update(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save()
            messages.success(request, "Project updated successfully.")
            return redirect(project.get_absolute_url())
    else:
        form = ProjectForm(instance=project)
    return render(request, "project_form.html", {**base_context(), "form": form, "project": project, "mode": "Update"})


@login_required
def project_delete(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if request.method == "POST":
        project.delete()
        messages.success(request, "Project removed successfully.")
        return redirect("dashboard")
    return render(request, "confirm_delete.html", {**base_context(), "object": project, "type": "project"})


@login_required
def project_sync_commit(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if project.sync_latest_commit():
        messages.success(request, "Latest GitHub commit synced.")
    else:
        messages.warning(request, "Could not sync commit. Check that the repository URL is a public GitHub repo.")
    return redirect("dashboard")


@login_required
def post_create(request):
    if request.method == "POST":
        form = ExternalPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.sync_preview(force=False)
            post.save()
            messages.success(request, "Post link saved and metadata synced.")
            return redirect("dashboard")
    else:
        form = ExternalPostForm()
    return render(request, "post_form.html", {**base_context(), "form": form, "mode": "Create"})


@login_required
def post_update(request, pk):
    post = get_object_or_404(ExternalPost, pk=pk)
    if request.method == "POST":
        form = ExternalPostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, "Post updated successfully.")
            return redirect("dashboard")
    else:
        form = ExternalPostForm(instance=post)
    return render(request, "post_form.html", {**base_context(), "form": form, "post": post, "mode": "Update"})


@login_required
def post_sync(request, pk):
    post = get_object_or_404(ExternalPost, pk=pk)
    post.sync_preview(force=True)
    post.save()
    messages.success(request, "Post metadata synced again.")
    return redirect("dashboard")


@login_required
def post_delete(request, pk):
    post = get_object_or_404(ExternalPost, pk=pk)
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post removed successfully.")
        return redirect("dashboard")
    return render(request, "confirm_delete.html", {**base_context(), "object": post, "type": "post"})


class OwnerLoginView(LoginView):
    template_name = "login.html"
    redirect_authenticated_user = True


def owner_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("home")
