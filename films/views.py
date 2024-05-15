from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponsePermanentRedirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.contrib.auth import get_user_model

from films.forms import RegisterForm


# Create your views here.
class IndexView(LoginView):
    template_name = "index.html"


class Login(LoginView):
    template_name = "registration/login.html"
