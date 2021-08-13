from allauth.account.views import LoginView
from django.urls import path

from accounts.views import (
    SignUpView,
    edit_profile,
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("edit-profile", edit_profile, name="edit-profile"),
]
