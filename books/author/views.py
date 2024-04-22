from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, FormView, CreateView, DeleteView, ListView, UpdateView, DetailView
from books.models import Author


class AuthorCreateView(PermissionRequiredMixin, CreateView):
    template_name = "create_author.html"
    model = Author
    fields = ['name', 'bio']
    success_url = reverse_lazy('author_list')
    login_url = 'login'
    permission_required = 'books.all_actions_author'


class AuthorListView(PermissionRequiredMixin, ListView):
    model = Author
    template_name = 'list_author.html'
    context_object_name = "authors"
    paginate_by = 5
    login_url = 'login'
    permission_required = 'books.all_actions_author'


class AuthorDeleteView(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('author_list')
    login_url = 'login'
    permission_required = 'books.all_actions_author'


class AuthorUpdateView(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = ['name', 'bio']
    template_name = 'update_author.html'
    success_url = reverse_lazy('author_list')
    context_object_name = 'author'
    login_url = 'login'
    permission_required = 'books.all_actions_author'


class AuthorDetailView(PermissionRequiredMixin, DetailView):
    model = Author
    template_name = "details_author.html"
    context_object_name = "author"
    login_url = 'login'
    permission_required = 'books.all_actions_author'