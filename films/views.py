from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.http.response import HttpResponse, HttpResponsePermanentRedirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.contrib.auth import get_user_model
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from films.forms import RegisterForm
from films.models import Film


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


class FilmList(LoginRequiredMixin, ListView):
    template_name = "films.html"
    model = Film
    context_object_name = "films"

    def get_queryset(self) -> QuerySet[Film]:
        user = self.request.user
        if user.is_authenticated:
            return user.films.all()
        else:
            return HttpResponseRedirect(reverse("login"))


# HTMX handles
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


@login_required
def add_film(request):
    name = request.POST.get("filmname")
    try:
        film = Film.objects.get_or_create(name=name)[0]
        # add the film to the user's list
        request.user.films.add(film)

        # return template with all of the user's films
        films = request.user.films.all()
        messages.success(request, f"Added {name} to list of films")
        return render(request, "partials/film-list.html", {"films": films})
    except Exception as error:
        print(error)


@login_required
@require_http_methods(["DELETE"])
def delete_film(request, pk):
    # remove the film from the user's list
    request.user.films.remove(pk)

    # return the template fragment
    films = request.user.films.all()
    return render(request, "partials/film-list.html", {"films": films})


@login_required
def search_film(request):
    search_text = request.POST.get("search")
    userfilms = request.user.films.all().values_list("name", flat=True)

    results = Film.objects.filter(name__icontains=search_text).exclude(
        name__in=userfilms
    )

    return render(request, "partials/search-results.html", {"results": results})

@login_required
def clear(request):
    return HttpResponse("")