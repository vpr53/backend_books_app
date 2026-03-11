from core.applications.accounts.dto import SendTokenResultDTO
from core.domain.accounts.entity import User
from core.domain.accounts.exeptions import (
    EmailNotVerifiedError,
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

        token = self.token_send_service.generate_and_save_token(user)

        u_id = UserId(user.user_id)
        self.token_send_service.send_token(email, u_id.encode(), token)

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

        if not self.token_send_service.check_token(user, token.value):
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
        user = self.repo.get_by_email(email)
        if not user:
            raise UserNotFoundError()

        if not user.is_email_verified:
            raise EmailNotVerifiedError()

        if not self.repo.is_verify_pass(email, password):
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

        token = self.token_send_service.generate_and_save_token(user)

        u_id = UserId(user.user_id)

        self.token_send_service.send_token(
            email=email, user_id=u_id.encode(), token=token
        )

        return SendTokenResultDTO(success=True)


class PasswordResetConfirmUseCase:
    def __init__(
        self, repo: BaseAccountsRepository, token_service: BaseTokenSenderService
    ):
        self.repo = repo
        self.token_service = token_service

    def execute(self, user_id: str, token: str):
        try:
            db_id = UserId.decode(user_id).value
        except ValueError:
            raise InvalidTokenError()

        user = self.repo.get_by_id(db_id)
        if not user:
            raise UserNotFoundError()

        token = Token(token)
        if not self.token_service.check_token(user, token):
            raise InvalidTokenError()

        return SendTokenResultDTO(success=True)


class PasswordResetCompleteUseCase:
    def __init__(
        self, repo: BaseAccountsRepository, token_service: BaseTokenSenderService
    ):
        self.repo = repo
        self.token_service = token_service

    def execute(self, user_id: str, token: str, password: str):
        try:
            db_id = UserId.decode(user_id).value
        except ValueError:
            raise InvalidTokenError()

        user = self.repo.get_by_id(db_id)
        if not user:
            raise UserNotFoundError()

        token = Token(token)
        if not self.token_service.check_token(user, token):
            raise InvalidTokenError()

        user.password = password
        self.repo.save(user)
