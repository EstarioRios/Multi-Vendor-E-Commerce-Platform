from django.urls import path
from .views import *


urlpatterns = [
    path("signup/", signup, name="SignUp"),
    path("login_manual", login_manual, name="login_manual"),
    path("login_JWT", login_JWT, name="login_JWT"),
    path("user_information", user_information, name="user_information"),
]
