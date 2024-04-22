from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, FormView, CreateView, DeleteView, ListView, UpdateView, DetailView
from books.models import Genre

class GenreCreateView(PermissionRequiredMixin, CreateView):
    template_name = "create_genre.html"
    model = Genre
    fields = ['name']
    success_url = reverse_lazy('genre_list')
    login_url = 'login'
    permission_required = 'books.all_actions_genre'


class GenreListView(PermissionRequiredMixin, ListView):
    model = Genre
    template_name = 'list_genre.html'
    context_object_name = "genres"
    paginate_by = 5
    login_url = 'login'
    permission_required = 'books.all_actions_genre'


class GenreDeleteView(PermissionRequiredMixin, DeleteView):
    model = Genre
    success_url = reverse_lazy('genre_list')
    login_url = 'login'
    permission_required = 'books.all_actions_genre'


class GenreUpdateView(PermissionRequiredMixin, UpdateView):
    model = Genre
    fields = ['name']
    template_name = 'update_genre.html'
    success_url = reverse_lazy('genre_list')
    context_object_name = 'genre'
    login_url = 'login'
    permission_required = 'books.all_actions_genre'