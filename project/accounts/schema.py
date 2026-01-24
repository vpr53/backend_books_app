from ninja import Schema, Field
from pydantic import EmailStr, Field



class RegisterSchema(Schema):
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password, min 8 chars")


class LoginSchema(Schema):
    email: EmailStr
    password: str = Field(..., description="Password")


class PasswordResetRequestSchema(Schema):
    email: EmailStr


class PasswordResetCompleteSchema(Schema):
    uid: str
    token: str
    new_password: str = Field(..., min_length=8, description="New password, min 8 chars")


class AcsessRefrashSchema(Schema):
    access: str
    refresh: str


class ErrorSchema(Schema):
    detail: str

class SuccessfulSchema(Schema):
    detail: str