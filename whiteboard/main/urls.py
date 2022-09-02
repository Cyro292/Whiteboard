from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.view_login, name="login"),
    path("logout", views.view_logout, name="logout"),
]
