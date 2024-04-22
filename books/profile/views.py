from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetDoneView
from django.urls import reverse, reverse_lazy
from books.forms import UserCreationForm
from django.views.generic import TemplateView, FormView, CreateView, DeleteView, ListView, UpdateView, DetailView

from books.models import NoticeBorrow


class Login(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return reverse('main')


class Logout(LoginRequiredMixin, LogoutView):
    login_url = 'login'

    def get_success_url(self):
        return reverse('main')


class Register(CreateView):
    form_class = UserCreationForm
    template_name = 'registration.html'
    success_url = reverse_lazy('main')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile.html"
    login_url = 'login'
