from django.urls import path
from books.profile.views import (Login,
                                 Logout,
                                 Register,
                                 ProfileView
                                 )


urlpatterns = [
    path("login/", Login.as_view(), name="login"),
    path("logout/", Logout.as_view(), name="logout"),
    path("registration/", Register.as_view(), name="register"),
    path("actions/", ProfileView.as_view(), name="profile"),
]