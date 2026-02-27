
from django.urls import path
from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController
from core.api.v1.urls import router as v1_router

api = NinjaExtraAPI(title="Book API", version="1.0.0")

api.register_controllers(NinjaJWTDefaultController)

api.add_router("/", v1_router)

urlpatterns = [
    path("", api.urls),
]