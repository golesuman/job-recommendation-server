from django.urls import path

from .views import UserLoginView, UserLogoutView, UserProfileAPI

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("logout/", UserLogoutView.as_view(), name="user_logout"),
    path("profile/", UserProfileAPI.as_view(), name="user_profile"),
]
