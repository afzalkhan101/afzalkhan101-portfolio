from django import forms

from .models import ExternalPost, Project, SiteProfile


class OdooStyledFormMixin:
    input_class = (
        "w-full rounded-2xl bg-white/5 border border-white/20 px-4 py-3 text-paper "
        "placeholder-muted focus:border-secondarylt focus:ring-2 focus:ring-secondary/20 outline-none transition"
    )
    textarea_class = input_class + " min-h-[120px]"
    select_class = input_class
    checkbox_class = "rounded border-white/20 bg-white/5 text-secondary focus:ring-secondary/40"

    def apply_styles(self):
        for name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs.update({"class": self.checkbox_class})
            elif isinstance(widget, forms.Textarea):
                widget.attrs.update({"class": self.textarea_class})
            else:
                widget.attrs.update({"class": self.input_class})


class SiteProfileForm(OdooStyledFormMixin, forms.ModelForm):
    class Meta:
        model = SiteProfile
        fields = [
            "name",
            "logo_text",
            "title",
            "role_highlight",
            "hero_badge",
            "bio",
            "about_long",
            "email",
            "github",
            "linkedin",
            "twitter",
            "youtube",
            "stats_text",
            "services_text",
            "focus_areas_text",
            "skills_text",
        ]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
            "about_long": forms.Textarea(attrs={"rows": 5}),
            "stats_text": forms.Textarea(attrs={"rows": 4}),
            "services_text": forms.Textarea(attrs={"rows": 5}),
            "focus_areas_text": forms.Textarea(attrs={"rows": 5}),
            "skills_text": forms.Textarea(attrs={"rows": 3}),
        }
        labels = {
            "stats_text": "Stats",
            "services_text": "Services",
            "focus_areas_text": "Focus Areas",
            "skills_text": "Skills",
        }
        help_texts = {
            "role_highlight": "This word will use the existing teal gradient in the hero title. Example: Odoo",
            "stats_text": "One stat per line: 6+ | Years Experience | ▰",
            "focus_areas_text": "One focus per line: ⚙️ | Odoo ERP | Description",
            "skills_text": "Use comma or new line separated skills.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["twitter"].required = False
        self.fields["youtube"].required = False
        self.apply_styles()


class ProjectForm(OdooStyledFormMixin, forms.ModelForm):
    features_text = forms.CharField(
        required=False,
        label="Features / Details",
        help_text="One feature per line. Example: Dynamic project CRUD - Add, edit and remove projects.",
        widget=forms.Textarea,
    )

    class Meta:
        model = Project
        fields = [
            "name",
            "short_desc",
            "detailed_description",
            "project_type",
            "status",
            "tech_stack",
            "repo_url",
            "live_url",
            "last_commit_message",
            "last_commit_hash",
            "last_commit_at",
            "is_featured",
            "display_order",
        ]
        widgets = {
            "detailed_description": forms.Textarea(attrs={"rows": 5}),
            "last_commit_at": forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["last_commit_at"].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"]
        if self.instance.pk:
            self.fields["features_text"].initial = "\n".join(
                feature.title + (f" - {feature.details}" if feature.details else "")
                for feature in self.instance.features.all()
            )
        self.apply_styles()

    def clean_features_text(self):
        value = self.cleaned_data.get("features_text", "")
        return "\n".join(line.strip() for line in value.splitlines() if line.strip())

    def save(self, commit=True):
        project = super().save(commit=commit)
        if commit:
            self.save_features(project)
        return project

    def save_features(self, project):
        from .models import ProjectFeature

        ProjectFeature.objects.filter(project=project).delete()
        features_text = self.cleaned_data.get("features_text", "")
        for index, line in enumerate(features_text.splitlines(), start=1):
            title, separator, details = line.partition(" - ")
            ProjectFeature.objects.create(
                project=project,
                title=title.strip(),
                details=details.strip() if separator else "",
                status="done",
                order=index,
            )


class ExternalPostForm(OdooStyledFormMixin, forms.ModelForm):
    class Meta:
        model = ExternalPost
        fields = ["url", "platform", "title", "description", "site_name", "is_visible", "display_order"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].required = False
        self.fields["description"].required = False
        self.fields["site_name"].required = False
        self.apply_styles()
