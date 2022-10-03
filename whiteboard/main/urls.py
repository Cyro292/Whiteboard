from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("signin", views.signin_view, name="signin"),
    path("signout", views.signout_view, name="signout"),
    path("register", views.register_view, name="register"),
    path("board/<str:id>", views.board_view, name="board"),
    path("boards", views.boards_view, name="boards"),
    path("addBoard/", views.add_board_view, name="add_board"),
    path("invite/<str:code>", views.invite_view, name="invite"),
]
