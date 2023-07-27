from django.urls import path
# <<<<<<< HEAD
# from .views import HomeView, Login, Logout, RegisterUser,Chats, NewComment, Like, Dislike
# =======
from .views import HomeView, Login, Logout, RegisterUser,Chats, NewComment, Like, Dislike, newPost, newImageProfile, settingProfile
# >>>>>>> 18bae8e79b277981680ffd2d1772896169ae1008
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", login_required(HomeView), name="books"),
    path("login/", Login, name="login"),
    path("logout/", Logout, name="logout"),
    path("register/", RegisterUser, name="register"),
    path("comment/<int:pid>", NewComment, name="comment"),
    path("like/<int:post_id>", Like, name="like_post"),
    path("dislike/<int:post_id>", Dislike, name="dislike_post"),
# <<<<<<< HEAD
# =======
    path("chat/", Chats, name="chat"),
    path("newPost/", newPost, name="newPost"),
    path("newImageProfile/", newImageProfile, name="imageProfile"),
    path("updateUser/", settingProfile, name="updateUser"),
# >>>>>>> 18bae8e79b277981680ffd2d1772896169ae1008
]
