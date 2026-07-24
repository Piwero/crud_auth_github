from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import (
    redirect,
    render,
)
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import (
    CustomUserChangeForm,
    CustomUserCreationForm,
)


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class EditProfileView(CreateView):
    form_class = CustomUserChangeForm
    success_url = reverse_lazy("home")
    template_name = "edit-profile.html"


def edit_profile(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    if not isinstance(request.user, AnonymousUser):
        if request.method == "POST":
            form = CustomUserChangeForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect("home")
        else:
            form = CustomUserChangeForm(instance=request.user)
        return render(request, "edit-profile.html", {"form": form})
    return render(request, "edit-profile.html")
