from django.contrib import admin

from .models import ExternalPost, Project, ProjectFeature, SiteProfile


@admin.register(SiteProfile)
class SiteProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "title", "email", "updated_at")
    fieldsets = (
        ("Main Identity", {"fields": ("name", "logo_text", "title", "role_highlight", "hero_badge")}),
        ("Content", {"fields": ("bio", "about_long", "stats_text", "services_text", "focus_areas_text", "skills_text")}),
        ("Links", {"fields": ("email", "github", "linkedin", "twitter", "youtube")}),
    )


class ProjectFeatureInline(admin.TabularInline):
    model = ProjectFeature
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "project_type", "status", "is_featured", "last_commit_at", "updated_at")
    list_filter = ("status", "is_featured", "project_type")
    search_fields = ("name", "short_desc", "tech_stack", "last_commit_message")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProjectFeatureInline]


@admin.register(ProjectFeature)
class ProjectFeatureAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "status", "order")
    list_filter = ("status",)
    search_fields = ("title", "details", "project__name")


@admin.register(ExternalPost)
class ExternalPostAdmin(admin.ModelAdmin):
    list_display = ("title", "platform", "site_name", "is_visible", "synced_at", "created_at")
    list_filter = ("platform", "is_visible")
    search_fields = ("title", "description", "url")
    actions = ["sync_selected_previews"]

    @admin.action(description="Sync metadata again for selected posts")
    def sync_selected_previews(self, request, queryset):
        updated = 0
        for post in queryset:
            if post.sync_preview(force=True):
                post.save()
                updated += 1
        self.message_user(request, f"Synced {updated} post preview(s).")
