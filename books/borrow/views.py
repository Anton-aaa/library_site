from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ImproperlyConfigured
from django.db.models import QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, FormView, CreateView, DeleteView, ListView, UpdateView, DetailView, RedirectView
from datetime import date
from books.forms import BorrowRequestApproveForm
from books.models import BorrowRequest, Book, NoticeBorrow



class BorrowRequestCreateView(LoginRequiredMixin, RedirectView):
    query_string = True
    pattern_name = 'borrow_success'

    def post(self, request, *args, **kwargs):
        book = Book.objects.filter(pk=self.kwargs['pk']).first()
        borrower = self.request.user
        status = 1
        # does the user have a borrow request for this book?
        old_borrow = BorrowRequest.objects.filter(book=book, borrower=borrower)
        for borrow in old_borrow:
            if borrow.status == 1 or borrow.status == 2 or borrow.status == 3:
                raise ValueError("User already has active borrow request for this book")

        borrow_request = BorrowRequest(book=book, borrower=borrower, status=status)
        borrow_request.save()
        return self.get(request, *args, **kwargs)


class BorrowRequestSuccessView(LoginRequiredMixin, TemplateView):
    template_name = "success_borrow.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = Book.objects.get(pk=self.kwargs['pk'])
        return context


class BorrowRequestListView(PermissionRequiredMixin, ListView):
    model = BorrowRequest
    template_name = 'list_borrow.html'
    context_object_name = "borrows"
    paginate_by = 5
    login_url = 'login'
    permission_required = 'books.process_request'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_form'] = BorrowRequestApproveForm()
        return context

class BorrowRequestApproveView(PermissionRequiredMixin, FormView):
    login_url = 'login'
    form_class = BorrowRequestApproveForm
    permission_required = 'books.process_request'
    success_url = reverse_lazy('borrow_list')


    def form_valid(self, form):
        borrow = BorrowRequest.objects.get(id=self.kwargs['pk'])
        book = borrow.book
        if borrow.status == 1:
            book.available = False
            book.borrower = borrow.borrower
            book.save()

            borrow.status = 2
            borrow.approval_date = datetime.date.today()
            borrow.due_date = form.cleaned_data['due_date']
            borrow.save()

            NoticeBorrow.objects.create(borrow_request=borrow, borrow_result=True)
            return super().form_valid(form)
        else:
            raise ValueError("Status not 'Pending'")


class BorrowRequestRejectView(PermissionRequiredMixin, CreateView):
    login_url = 'login'
    model = NoticeBorrow
    fields = ['refusal_message',]
    template_name = "reject_borrow_request.html"
    permission_required = 'books.process_request'
    success_url = reverse_lazy('borrow_list')


    def form_valid(self, form):
        borrow = BorrowRequest.objects.get(id=self.kwargs['pk'])
        notice = form.save(commit=False)
        if borrow.status == 1:
            borrow.status = 5
            borrow.save()
            notice.borrow_request = borrow
            notice.borrow_result = False
            return super().form_valid(form)
        else:
            raise ValueError("Status not 'Pending'")


class BorrowRequestCompleteView(PermissionRequiredMixin, View):
    login_url = 'login'
    permission_required = 'books.process_request'
    http_method_names = ['post', ]

    def post(self, request, *args, **kwargs):
        borrow = BorrowRequest.objects.get(id=self.kwargs['pk'])
        book = borrow.book
        if borrow.status == 2 or borrow.status == 3:
            book.available = True
            book.borrower = None
            book.save()
            borrow.status = 4
            borrow.complete_date = datetime.date.today()
            borrow.save()
            return HttpResponseRedirect(reverse_lazy('borrow_list'))

        raise ValueError("Status not 'Approved' or 'Collected'")


class BorrowRequestUserListView(LoginRequiredMixin, ListView):
    model = BorrowRequest
    template_name = 'list_borrow_user.html'
    context_object_name = "borrows"
    paginate_by = 5
    login_url = 'login'

    def get_queryset(self):
        if self.queryset is not None:
            queryset = self.queryset
            if isinstance(queryset, QuerySet):
                queryset = queryset.all()
        elif self.model is not None:
            queryset = self.model._default_manager.filter(borrower=self.request.user)
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


class BorrowRequestTakeView(LoginRequiredMixin, View):
    login_url = 'login'
    http_method_names = ['post', ]


    def post(self, request, *args, **kwargs):
        borrow = BorrowRequest.objects.get(id=self.kwargs['pk'])
        if borrow.borrower == self.request.user:
            if borrow.status == 2:
                borrow.status = 3
                borrow.save()
                return render(request, 'success_take.html', {"book": borrow.book})
            else:
                raise ValueError("Status not 'Approved'")

        raise ValueError("This borrow request does not apply to this user")


class BorrowRequestDetailView(DetailView):
    model = BorrowRequest
    template_name = "details_borrow.html"
    context_object_name = "borrow"


class BorrowRequestDeadlineTrackingView(PermissionRequiredMixin, ListView):
    model = BorrowRequest
    template_name = 'list_overdue_borrow.html'
    context_object_name = "borrows"
    paginate_by = 5
    login_url = 'login'
    permission_required = 'books.process_request'

    def get_queryset(self):
        if self.queryset is not None:
            queryset = self.queryset
            if isinstance(queryset, QuerySet):
                queryset = queryset.all()
        elif self.model is not None:
            for borrow in BorrowRequest.objects.filter(status=2):
                if borrow.due_date < date.today():
                    borrow.overdue = True
                    borrow.save()
            for borrow in BorrowRequest.objects.filter(status=3):
                if borrow.due_date < date.today():
                    borrow.overdue = True
                    borrow.save()
            queryset = self.model._default_manager.filter(overdue=True)
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
