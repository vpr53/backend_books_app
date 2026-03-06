from dataclasses import dataclass
from abc import ABC, abstractmethod
from .entity import User

class BaseAccountsRepository(ABC):
    @abstractmethod
    def exists(self, email: str)-> bool:
        ...

    @abstractmethod
    def create(self, email: str, password: str)-> User:
        ...
    
    @abstractmethod
    def save(self, user: User)-> None:
        ...

    @abstractmethod
    def get_by_id(self, id: int) -> User | None:
        ...
    
    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        ...

    @abstractmethod
    def is_verify_pass(self, user: User, password: str)-> bool: 
        ...
    
 
    