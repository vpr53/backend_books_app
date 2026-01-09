from django.contrib import admin
from accounts.models import User
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "is_active", "is_staff", "is_email_verified"]





