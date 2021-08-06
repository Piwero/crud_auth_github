from django.contrib import admin

from .forms import (
    CustomUserChangeForm,
    CustomUserCreationForm,
)
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
