from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
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
from django.conf import settings

from films.forms import RegisterForm
from films.models import Film, UserFilms
from films.utils import get_max_order, reorder


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
    model = UserFilms
    paginate_by = settings.PAGINATE_BY
    context_object_name = "films"

    def get_template_names(self):
        if self.request.htmx:
            return "partials/film-list-elements.html"
        return "films.html"

    def get_queryset(self) -> QuerySet[Film]:
        return UserFilms.objects.prefetch_related("film").filter(user=self.request.user)


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
        if not UserFilms.objects.filter(film=film, user=request.user).exists():
            UserFilms.objects.create(
                film=film, user=request.user, order=get_max_order(request.user)
            )

        # return template with all of the user's films
        films = UserFilms.objects.filter(user=request.user)
        messages.success(request, f"Added {name} to list of films")
        return render(request, "partials/film-list.html", {"films": films})
    except Exception as error:
        print(error)


@login_required
@require_http_methods(["DELETE"])
def delete_film(request, pk):
    # remove the film from the user's list
    UserFilms.objects.get(pk=pk).delete()
    reorder(user=request.user)
    # return the template fragment
    films = UserFilms.objects.filter(user=request.user)
    return render(request, "partials/film-list.html", {"films": films})


@login_required
def search_film(request):
    search_text = request.POST.get("search")
    userfilms = UserFilms.objects.filter(user=request.user).values_list(
        "film__name", flat=True
    )

    results = Film.objects.filter(name__icontains=search_text).exclude(
        name__in=userfilms
    )

    return render(request, "partials/search-results.html", {"results": results})


@login_required
def clear(request):
    return HttpResponse("")


@login_required
def sort(request):
    film_pks_order = request.POST.getlist("film_order")
    films = []
    for index, film_pk in enumerate(film_pks_order, start=1):
        userfilm = UserFilms.objects.get(pk=film_pk)
        userfilm.order = index
        userfilm.save()
        films.append(userfilm)

    return render(request, "partials/film-list.html", {"films": films})


@login_required
def detail(request, pk):
    userfilm = get_object_or_404(UserFilms, pk=pk)
    return render(request, "partials/film-detail.html", {"userfilm": userfilm})


@login_required
def films_parital(request):
    films = UserFilms.objects.filter(user=request.user)
    return render(request, "partials/film-list.html", {"films": films})


@login_required
def upload_photo(request, pk):
    userfilm = get_object_or_404(UserFilms, pk=pk)
    photo = request.FILES.get("photo")
    userfilm.film.photo.save(photo.name, photo)

    return render(request, "partials/film-detail.html", {"userfilm": userfilm})
