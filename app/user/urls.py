"""
URL mappings for the user API.
"""
from django.urls import path

from user import views

# reverseで指定するapp名
app_name = "user"

# nameはreveseで指定する名前
urlpatterns = [
    path("create/", views.CreateUserView.as_view(), name="create"),
    path("token/", views.CreateTokenView.as_view(), name="token"),
    path("me/", views.ManageUserView.as_view(), name="me"),
]
