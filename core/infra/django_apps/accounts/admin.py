from django.contrib import admin
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)

from core.infra.django_apps.accounts.models import UserModels


@admin.register(UserModels)
class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "is_active", "is_staff", "is_email_verified"]


admin.site.unregister(BlacklistedToken)
admin.site.unregister(OutstandingToken)
