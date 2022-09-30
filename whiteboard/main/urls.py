from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signin", views.signin, name="signin"),
    path("signout", views.signout, name="signout"),
    path("register", views.register, name="register"),
    path("board/<str:id>", views.board, name="board"),
    path("boards", views.boards, name="boards"),
    path("addBoard/", views.add_board, name="add_board"),
    path("invite/<str:code>", views.invite, name="invite"),
]
