from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ImproperlyConfigured
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView, CreateView, DeleteView, ListView, UpdateView, DetailView, RedirectView
from books.forms import BorrowRequestApproveForm
from books.models import NoticeBorrow
from django.db.models import F


class NoticeBorrowUserListView(LoginRequiredMixin, ListView):
    model = NoticeBorrow
    template_name = 'list_notice_borrow_user.html'
    context_object_name = "notices"
    paginate_by = 5
    login_url = 'login'

    def get_queryset(self):
        if self.queryset is not None:
            queryset = self.queryset
            if isinstance(queryset, QuerySet):
                queryset = queryset.all()
        elif self.model is not None:
            queryset = self.model._default_manager.filter(borrow_request__borrower=self.request.user)
        else:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {"cls": self.__class__.__name__}
            )
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        return queryset


class NoticeBorrowUserReadView(LoginRequiredMixin, View):
    login_url = 'login'
    permission_required = 'books.process_request'
    http_method_names = ['post', ]

    def post(self, request, *args, **kwargs):
        NoticeBorrow.objects.filter(borrow_request__borrower=self.request.user, viewed=False).update(viewed=True)
        return HttpResponseRedirect(reverse_lazy('notice_borrow_list'))
