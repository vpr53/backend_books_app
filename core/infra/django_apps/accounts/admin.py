from django.contrib import admin
from core.infra.django_apps.accounts.models import UserModels
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken


@admin.register(UserModels)
class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "is_active", "is_staff", "is_email_verified"]


admin.site.unregister(BlacklistedToken)
admin.site.unregister(OutstandingToken)



