"""
Definition of the blog app. URLs
"""

from django.urls import path
from django.contrib.auth import views as authViews
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.PostList.as_view(), name="journal"),
    path("<int:pk>", views.PostDetail.as_view(), name="article"),
    path("sign_in", authViews.LoginView.as_view(), name="login"),
    path("sign_up", views.subscription, name="subscribe"),
    path("<int:pk>/edit", views.EditPost.as_view(), name="edit"),
    path("<int:pk>/delete", views.DeletePost.as_view(), name="delete"),
    path("<int:pk>/remove", views.removeComment, name="remove"),
    path("new", views.NewPost.as_view(), name="create"),
    path("drafts", views.DraftList.as_view(), name="drafts"),
    path("sign_out", authViews.LogoutView.as_view(), name="logout")
]
