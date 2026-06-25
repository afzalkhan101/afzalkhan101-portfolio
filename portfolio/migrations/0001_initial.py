# Generated manually for the dynamic portfolio update.

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=160)),
                ('slug', models.SlugField(blank=True, max_length=180, unique=True)),
                ('short_desc', models.CharField(max_length=240, verbose_name='Short description')),
                ('detailed_description', models.TextField(blank=True)),
                ('project_type', models.CharField(blank=True, help_text='Example: Odoo Module, Django App, SaaS', max_length=120)),
                ('status', models.CharField(choices=[('planning', 'Planning'), ('active', 'Active'), ('paused', 'Paused'), ('completed', 'Completed'), ('archived', 'Archived')], default='active', max_length=20)),
                ('tech_stack', models.CharField(blank=True, help_text='Comma separated: Odoo, Python, PostgreSQL', max_length=400)),
                ('repo_url', models.URLField(blank=True, verbose_name='GitHub / repository URL')),
                ('live_url', models.URLField(blank=True)),
                ('image_url', models.URLField(blank=True)),
                ('last_commit_message', models.CharField(blank=True, max_length=255)),
                ('last_commit_hash', models.CharField(blank=True, max_length=80)),
                ('last_commit_at', models.DateTimeField(blank=True, null=True)),
                ('is_featured', models.BooleanField(default=True)),
                ('display_order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['display_order', '-last_commit_at', '-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='ExternalPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(unique=True)),
                ('platform', models.CharField(choices=[('blog', 'Blog'), ('linkedin', 'LinkedIn'), ('medium', 'Medium'), ('devto', 'Dev.to'), ('hashnode', 'Hashnode')], default='blog', max_length=20)),
                ('title', models.CharField(blank=True, max_length=250)),
                ('description', models.TextField(blank=True)),
                ('image_url', models.URLField(blank=True)),
                ('site_name', models.CharField(blank=True, max_length=120)),
                ('is_visible', models.BooleanField(default=True)),
                ('display_order', models.PositiveIntegerField(default=0)),
                ('synced_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['display_order', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ProjectFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=180)),
                ('details', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('todo', 'Todo'), ('progress', 'In Progress'), ('done', 'Done'), ('future', 'Future')], default='done', max_length=20)),
                ('order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='features', to='portfolio.project')),
            ],
            options={
                'ordering': ['order', 'id'],
            },
        ),
    ]
