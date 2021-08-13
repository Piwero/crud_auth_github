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

    def form_valid(self, form, request):
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

            return redirect("home")
        else:
            form = CustomUserChangeForm(instance=request.user)
            return render(request, "edit-profile.html", {"form": form})


def edit_profile(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

            return redirect("home")
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, "edit-profile.html", {"form": form})
