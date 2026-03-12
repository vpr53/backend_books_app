from core.domain.accounts.entity import User
from core.domain.accounts.exeptions import (
    InvalidTokenError,
    UserNotFoundError,
)
from core.domain.accounts.repository import BaseAccountsRepository
from core.domain.accounts.service import (
    BaseTokenSenderService,
)
from core.domain.accounts.value_objects import Token, UserId


class TokenValidatorService:
    def __init__(
        self, repo: BaseAccountsRepository, token_service: BaseTokenSenderService
    ):
        self.repo = repo
        self.token_service = token_service

    def validate_user_and_token(self, user_id: str, token_str: str) -> User:
        try:
            db_id = UserId.decode(user_id)
        except ValueError:
            raise InvalidTokenError()

        user = self.repo.get_by_id(db_id)
        if not user:
            raise UserNotFoundError()

        token = Token(token_str)
        if not self.token_service.check_token(user, token):
            raise InvalidTokenError()

        return user
