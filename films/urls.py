from django.urls import path
from django.contrib.auth.views import LoginView

from films import views

urlpatterns = [
    path("index/", views.IndexView.as_view(), name="index"),
    path("login/", views.IndexView.as_view(), name="login"),
    path("logout/", views.IndexView.as_view(), name="logout"),
    path("register/", views.IndexView.as_view(), name="register"),
]
