from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
from passlib.hash import bcrypt
from .value_objects import UserId

@dataclass
class User:
    user_id: UserId
    email: str
    password: str
    is_active: bool = False
    is_staff: bool = False
    is_email_verified: bool = False
    is_superuser: bool = False
    date_joined: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def activate(self):
        self.is_active = True

    def verify_email(self):
        self.is_email_verified = True

    def promote_to_staff(self):
        self.is_staff = True
    
    # def verify_password(self, raw_password: str) -> bool:
    #     return bcrypt.verify(raw_password, self.password_hash)
    
    # def hash_password(self, password: str):
    #     return bcrypt.hash(password)

