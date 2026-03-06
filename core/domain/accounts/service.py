from abc import ABC, abstractmethod
from core.domain.accounts.entity import User
from core.domain.accounts.value_objects import Token, UserId

class BaseTokenSenderService(ABC):
    
    @abstractmethod
    def send_token(self, email: str, user_id: UserId, token: Token) -> None:
        pass
    
    @abstractmethod
    def generate_and_save_token(self, user: User)-> Token:
        pass
    
    @abstractmethod
    def check_token(self, user: User, token: Token)-> bool:
        pass

