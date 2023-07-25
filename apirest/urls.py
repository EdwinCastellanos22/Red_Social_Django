from django.urls import path
from .views import HomeView, Login, Logout, RegisterUser,Chats, NewComment, Like, Dislike
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", login_required(HomeView.as_view()), name="books"),
    path("login/", Login, name="login"),
    path("logout/", Logout, name="logout"),
    path("register/", RegisterUser, name="register"),
    path("comment/<int:pid>", NewComment, name="comment"),
    path("like/<int:post_id>", Like, name="like_post"),
    path("dislike/<int:post_id>", Dislike, name="dislike_post"),
    path("chat/", Chats, name="chat")
]
