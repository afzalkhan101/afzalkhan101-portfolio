from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/login/", views.OwnerLoginView.as_view(), name="dashboard_login"),
    path("dashboard/logout/", views.owner_logout, name="dashboard_logout"),
    path("dashboard/profile/", views.profile_update, name="profile_update"),
    path("projects/create/", views.project_create, name="project_create"),
    path("projects/<slug:slug>/", views.project_detail, name="project_detail"),
    path("projects/<slug:slug>/edit/", views.project_update, name="project_update"),
    path("projects/<slug:slug>/sync-commit/", views.project_sync_commit, name="project_sync_commit"),
    path("projects/<slug:slug>/delete/", views.project_delete, name="project_delete"),
    path("posts/create/", views.post_create, name="post_create"),
    path("posts/<int:pk>/edit/", views.post_update, name="post_update"),
    path("posts/<int:pk>/sync/", views.post_sync, name="post_sync"),
    path("posts/<int:pk>/delete/", views.post_delete, name="post_delete"),
]
