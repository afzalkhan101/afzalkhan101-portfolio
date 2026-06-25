# Generated manually for dynamic owner/profile content.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="SiteProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(default="Afzal Khan", max_length=120)),
                ("logo_text", models.CharField(default="AK", max_length=12)),
                ("title", models.CharField(default="Senior Odoo Developer", max_length=160)),
                ("role_highlight", models.CharField(default="Odoo", max_length=80)),
                ("hero_badge", models.CharField(default="Available for new opportunities", max_length=160)),
                ("bio", models.TextField(default="I build robust, scalable and business-driven solutions with Odoo. From custom modules to full ERP implementations, I help businesses grow smarter.")),
                ("about_long", models.TextField(default="I am focused on Odoo ERP customization, Django backend development, clean business workflows, and practical modules that solve real company problems. This portfolio tracks my projects, features, tech stack, last commit notes and published writing in one premium dashboard.")),
                ("email", models.EmailField(default="afzalkhan101@gmail.com", max_length=254)),
                ("github", models.URLField(blank=True, default="https://github.com/afzalkhan101")),
                ("linkedin", models.URLField(blank=True, default="https://www.linkedin.com/")),
                ("twitter", models.CharField(blank=True, default="#", max_length=255)),
                ("youtube", models.CharField(blank=True, default="#", max_length=255)),
                ("profile_picture", models.FileField(blank=True, upload_to="profile/")),
                ("stats_text", models.TextField(default="6+ | Years Experience | ▰\n40+ | Modules Built | ✦\n20+ | Happy Clients | ↗", help_text="One stat per line: value | label | icon")),
                ("services_text", models.TextField(default="Custom Module Development\nOdoo Implementation\nOdoo Integration\nPerformance Optimization", help_text="One service per line.")),
                ("focus_areas_text", models.TextField(default="⚙️ | Odoo ERP | Custom modules, reports, approval workflows and business automation.\n🐍 | Django Backend | Database-driven apps, dashboards, forms and clean admin tools.\n📊 | Business Systems | Accounting, sales, inventory and operations-focused workflows.", help_text="One focus area per line: icon | label | description")),
                ("skills_text", models.TextField(default="Odoo, Python, Django, PostgreSQL, JavaScript, Tailwind CSS, Docker, Nginx", help_text="Comma or line separated skills.")),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Site Profile",
                "verbose_name_plural": "Site Profile",
            },
        ),
    ]
