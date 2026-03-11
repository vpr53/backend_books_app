from core.domain.accounts.entity import User
from core.domain.accounts.repository import BaseAccountsRepository

from .models import UserModels


class DjangoAccountsRepository(BaseAccountsRepository):
    def _to_entity(self, db_user: UserModels) -> User:
        return User(
            user_id=db_user.id,
            email=db_user.email,
            is_active=db_user.is_active,
            is_superuser=db_user.is_superuser,
            is_staff=db_user.is_staff,
            is_email_verified=db_user.is_email_verified,
            password=db_user.password,
        )

    def exists(self, email: str) -> bool:
        return UserModels.objects.filter(email=email).exists()

    def create(self, email: str, password: str) -> User:
        db_user = UserModels.objects.create_user(email=email, password=password)
        return self._to_entity(db_user=db_user)

    def save(self, user: User) -> None:
        models_user = UserModels.objects.filter(id=user.user_id).first()

        models_user.email = user.email
        models_user.is_active = user.is_active
        models_user.is_superuser = user.is_superuser
        models_user.is_staff = user.is_staff
        models_user.is_email_verified = user.is_email_verified
        models_user.set_password(user.password)

        models_user.save()

    def get_by_id(self, id: int) -> User | None:
        db_user = UserModels.objects.filter(id=id).first()
        return self._to_entity(db_user)

    def get_by_email(self, email: str):
        db_user = UserModels.objects.filter(email=email).first()
        return self._to_entity(db_user)

    def is_verify_pass(self, email: str, password: str) -> bool:
        db_user = UserModels.objects.filter(email=email).first()

        return db_user.check_password(password)

    def get_django_user_by_id(self, user_id: int):
        return UserModels.objects.get(id=user_id)
