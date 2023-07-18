from django.urls import path
from .views import check, updateImage

urlpatterns= [
    path("", check, name="check"),
    path("update", updateImage, name="update")
]