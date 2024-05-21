from django.urls import path
from django.contrib.auth.views import LogoutView

from films import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("index/", views.IndexView.as_view(), name="index"),
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("my-films/", views.Myfilms.as_view(), name="my-films"),
]

htmx_urlpatterns = [
    path("check-username/", views.check_username, name="check-username")
]

urlpatterns += htmx_urlpatterns
