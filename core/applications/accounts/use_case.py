from core.applications.accounts.dto import SendTokenResultDTO
from core.applications.accounts.service import TokenValidatorService
from core.domain.accounts.entity import User
from core.domain.accounts.exeptions import (
    InvalidTokenError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from core.domain.accounts.repository import BaseAccountsRepository
from core.domain.accounts.service import (
    BaseTokenSenderService,
)
from core.domain.accounts.value_objects import Token, UserId


class RegisterUseCase:
    def __init__(
        self,
        repo: BaseAccountsRepository,
        token_send_service: BaseTokenSenderService,
    ):
        self.repo = repo
        self.token_send_service = token_send_service

    def execute(self, email: str, password: str):
        if self.repo.exists(email):
            raise UserAlreadyExistsError()

        user: User = self.repo.create(email, password)

        self.repo.save(user)

        token = self.token_send_service.generate_token(user)

        self.token_send_service.send_token(email, user.user_id.encode(), token)

        return user


class VerifyEmailUseCase:
    def __init__(
        self,
        repo: BaseAccountsRepository,
        token_send_service: BaseTokenSenderService,
    ):
        self.repo = repo
        self.token_send_service = token_send_service

    def execute(self, user_id: str, token_str: str):
        try:
            db_id = UserId.decode(user_id)
        except ValueError:
            raise InvalidTokenError()

        user = self.repo.get_by_id(db_id.value)
        if not user:
            raise UserNotFoundError()

        token = Token(token_str)
        if not self.token_send_service.check_token(user, token):
            raise InvalidTokenError()

        user.verify_email()
        self.repo.save(user)
        return SendTokenResultDTO(success=True)


class LoginUseCase:
    def __init__(
        self,
        repo: BaseAccountsRepository,
    ):
        self.repo = repo

    def execute(self, email: str, password: str):
        user = self.repo.is_verify_pass(
            email,
            password,
        )
        if not user:
            raise UserNotFoundError()
        return user


class PasswordResetUseCase:
    def __init__(
        self,
        repo: BaseAccountsRepository,
        token_send_service: BaseTokenSenderService,
    ):
        self.repo = repo
        self.token_send_service = token_send_service

    def execute(self, email: str):
        user = self.repo.get_by_email(email)
        if not user:
            raise UserNotFoundError()

        token = self.token_send_service.generate_token(user)

        self.token_send_service.send_token(
            email=email, user_id=user.user_id.encode(), token=token
        )

        return SendTokenResultDTO(success=True)


class PasswordResetConfirm:
    def __init__(self, validator: TokenValidatorService):
        self.validator = validator

    def execute(self, user_id: str, token: str):
        self.validator.validate_user_and_token(user_id, token)
        return SendTokenResultDTO(success=True)


class PasswordResetCompleteUseCase:
    def __init__(self, validator: TokenValidatorService, repo: BaseAccountsRepository):
        self.validator = validator
        self.repo = repo

    def execute(self, user_id: str, token: str, password: str):
        user = self.validator.validate_user_and_token(user_id, token)

        user.password = password
        self.repo.save(user)
