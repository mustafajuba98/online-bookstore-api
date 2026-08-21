from django.urls import path

from apps.users.endpoints.login.api import login_api
from apps.users.endpoints.refresh.api import refresh_api
from apps.users.endpoints.register.api import register_api

urlpatterns = [
    path("register/", register_api, name="register"),
    path("login/", login_api, name="login"),
    path("refresh/", refresh_api, name="refresh"),
]
