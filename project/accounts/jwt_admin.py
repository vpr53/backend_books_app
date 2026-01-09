from django.contrib import admin
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken


class OutstandingTokenProxy(OutstandingToken):
    class Meta:
        proxy = True
        verbose_name = "Активный токен"
        verbose_name_plural = "Активные токены"


@admin.register(OutstandingTokenProxy)
class OutstandingTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'created_at')


class BlacklistedTokenProxy(BlacklistedToken):
    class Meta:
        proxy = True
        verbose_name = "Заблокированный токен"
        verbose_name_plural = "Заблокированные токены"


@admin.register(BlacklistedTokenProxy)
class BlacklistedTokenAdmin(admin.ModelAdmin):
    list_display = ('token', 'blacklisted_at')