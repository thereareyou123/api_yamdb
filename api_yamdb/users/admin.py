from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'role', 'first_name', 'last_name', 'bio'
    )
