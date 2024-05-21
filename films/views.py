from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponsePermanentRedirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.contrib.auth import get_user_model

from films.forms import RegisterForm


# Create your views here.
class IndexView(TemplateView):
    template_name = "index.html"


class Login(LoginView):
    template_name = "registration/login.html"


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form: RegisterForm) -> HttpResponse:
        form.save()
        return super().form_valid(form)


def check_username(request):
    username = request.POST.get("username")
    if username == "":
        return HttpResponse("")
    elif get_user_model().objects.filter(username=username).exists():
        return HttpResponse(
            "<div id='username-error' class='red' >This username already exists</div>"
        )
    else:
        return HttpResponse(
            "<div id='username-error' class='primary' >This username is available</div>"
        )
class Myfilms(TemplateView):
    template_name ="films.html"