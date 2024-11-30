# === django import === #
from django.urls import path
from django.contrib.auth.decorators import login_required

# === app import === #
from apps.multilogin.views import LoginView, ProfileListView, ProfileDataView

urlpatterns = [
    path(
        "",
        login_required(ProfileListView.as_view(
            template_name="profile_list.html")),
        name="index"
    ),
    path(
        "multilogin/profile/data/",
        login_required(ProfileDataView.as_view()),
        name="profiles-data",
    ),
    path(
        "multilogin/login/",
        login_required(LoginView.as_view()),
        name="multilogin"
    ),
]
