from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        
        email = self.normalize_email(email)

        user = self.model(
        email=email,
        is_active=False,              
        is_email_verified=False,      
        **extra_fields
        )        
        
        user.set_password(password)
        user.save()
        return user

def create_superuser(self, email, password=None, **extra_fields):
    extra_fields.setdefault("is_staff", True)
    extra_fields.setdefault("is_superuser", True)
    extra_fields.setdefault("is_active", True)
    extra_fields.setdefault("is_email_verified", True)

    return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email