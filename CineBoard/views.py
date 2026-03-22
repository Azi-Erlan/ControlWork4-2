from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from .models import Film, Comment, Genre


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'


class FilmListView(ListView):
    model = Film
    template_name = 'film_list.html'
    context_object_name = 'films'

    def get_queryset(self):
        queryset = Film.objects.all()

        search = self.request.GET.get('q')
        genre = self.request.GET.get('genre')

        if search:
            search = search.strip()
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )

        if genre:
            queryset = queryset.filter(genre__name=genre)

        return queryset.order_by('-rating')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        return context


class FilmDetailView(DetailView):
    model = Film
    template_name = 'film_detail.html'


class FilmCreateView(LoginRequiredMixin, CreateView):
    model = Film
    fields = ['title', 'description', 'genre', 'release_date', 'tags', 'image']
    template_name = 'film_form.html'
    success_url = reverse_lazy('film_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class FilmUpdateView(LoginRequiredMixin, UpdateView):
    model = Film
    fields = ['title', 'description', 'genre', 'release_date', 'tags', 'image']
    template_name = 'film_form.html'
    success_url = reverse_lazy('film_list')


class FilmDeleteView(LoginRequiredMixin, DeleteView):
    model = Film
    template_name = 'film_confirm_delete.html'
    success_url = reverse_lazy('film_list')


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['text']

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.film_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('film_detail', kwargs={'pk': self.kwargs['pk']})