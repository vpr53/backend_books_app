from ninja import Router
from ninja.errors import HttpError
from ninja_jwt.tokens import RefreshToken

from core.applications.accounts.use_case import (
    LoginUseCase,
    PasswordResetCompleteUseCase,
    PasswordResetConfirmUseCase,
    PasswordResetUseCase,
    RegisterUseCase,
    VerifyEmailUseCase,
)
from core.domain.accounts.exeptions import (
    InvalidTokenError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from core.infra.django_apps.accounts.repository import DjangoAccountsRepository
from core.infra.django_apps.accounts.schema import (
    AcsessRefrashSchema,
    ErrorSchema,
    LoginSchema,
    PasswordResetCompleteSchema,
    PasswordResetInSchema,
    RegisterSchema,
    SuccessfulSchema,
)
from core.infra.django_apps.accounts.service.service import (
    EmailVerifySenderService,
    VerifyPasswordSenderService,
)

api = Router(tags=["Auth"])


@api.post("/register/", response={201: SuccessfulSchema, 409: ErrorSchema})
def register(request, payload: RegisterSchema):
    use_case = RegisterUseCase(
        repo=DjangoAccountsRepository(),
        token_send_service=EmailVerifySenderService(),
    )
    try:
        use_case.execute(payload.email, payload.password)
    except UserAlreadyExistsError:
        raise HttpError(409, "Email already registered")

    return 201, {"detail": "Check your email to verify account"}


@api.get(
    "/verify-email/",
    response={
        200: SuccessfulSchema,
        400: ErrorSchema,
    },
    summary="Подтверждение email",
    description="Проверяет ссылку подтверждения email и активирует пользователя",
)
def verify_email(request, uid: str, token: str):
    use_case = VerifyEmailUseCase(
        repo=DjangoAccountsRepository(),
        token_send_service=EmailVerifySenderService(),
    )
    try:
        use_case.execute(uid, token)
    except InvalidTokenError:
        raise HttpError(400, "Invalid verification link")

    except UserNotFoundError:
        raise HttpError(400, "Invalid or expired token")

    return {"detail": "Email successfully verified"}


@api.post("/login/", response={200: AcsessRefrashSchema, 400: ErrorSchema})
def login(request, payload: LoginSchema):
    repo = DjangoAccountsRepository()
    use_case = LoginUseCase(repo=repo)

    try:
        user = use_case.execute(payload.email, payload.password)
    except UserNotFoundError:
        raise HttpError(400, "Email or password not valid")

    dj_user = repo.get_django_user_by_id(user_id=user.user_id)
    refresh = RefreshToken.for_user(dj_user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


@api.post("password-reset/", response={200: SuccessfulSchema})
def password_reset(request, payload: PasswordResetInSchema):
    use_case = PasswordResetUseCase(
        repo=DjangoAccountsRepository(),
        token_send_service=VerifyPasswordSenderService(),
    )
    try:
        use_case.execute(payload.email)
    except UserNotFoundError:
        return {"detail": "If account exists, email was sent"}
    return {"detail": "If account exists, email was sent"}


@api.get("password-reset/confirm/", response={200: SuccessfulSchema, 400: ErrorSchema})
def password_reset_confirm(request, uid, token):
    use_case = PasswordResetConfirmUseCase(
        repo=DjangoAccountsRepository(),
        token_service=VerifyPasswordSenderService(),
    )
    try:
        use_case.execute(user_id=uid, token=token)
    except UserNotFoundError:
        raise HttpError(400, "Invalid or expired token")
    except InvalidTokenError:
        raise HttpError(400, "Invalid link")

    return 200, {"detail": "Token valid"}


@api.post(
    "password-reset/complete/", response={200: SuccessfulSchema, 400: ErrorSchema}
)
def password_reset_complete(request, payload: PasswordResetCompleteSchema):
    use_case = PasswordResetCompleteUseCase(
        repo=DjangoAccountsRepository(),
        token_service=VerifyPasswordSenderService(),
    )
    try:
        use_case.execute(
            user_id=payload.uid, token=payload.token, password=payload.new_password
        )
    except UserNotFoundError:
        raise HttpError(400, "Invalid or expired token")
    except InvalidTokenError:
        raise HttpError(400, "Invalid link")

    return {"detail": "Password successfully updated"}
