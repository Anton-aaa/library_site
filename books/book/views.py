from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, FormView, CreateView, DeleteView, ListView, UpdateView, DetailView
from books.models import Book, BorrowRequest


class BookCreateView(PermissionRequiredMixin, CreateView):
    template_name = "create_book.html"
    model = Book
    fields = ['title',
              'summary',
              'isbn',
              'published_date',
              'publisher',
              'genre',
              'author']
    success_url = reverse_lazy('book_list')
    login_url = 'login'
    permission_required = 'books.all_actions_book'


class BookListView(ListView):
    model = Book
    template_name = 'list_book.html'
    context_object_name = "books"
    paginate_by = 5


class BookDetailView(DetailView):
    model = Book
    template_name = "details_book.html"
    context_object_name = "book"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # does the user have a borrow request for this book?
        if self.request.user.is_authenticated:
            book = Book.objects.filter(pk=self.kwargs['pk']).first()
            borrows = BorrowRequest.objects.filter(book=book, borrower=self.request.user)
            for borrow in borrows:
                if borrow.status == 1 or borrow.status == 2 or borrow.status == 3:
                    print(borrow)
                    print(borrow.status)
                    context["borrow"] = True
                    return context

        context["borrow"] = False
        return context


class BookDeleteView(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('book_list')
    login_url = 'login'
    permission_required = 'books.all_actions_book'


class BookUpdateView(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = ['title',
              'summary',
              'isbn',
              'published_date',
              'publisher',
              'genre',
              'author']
    template_name = 'update_book.html'
    success_url = reverse_lazy('book_list')
    context_object_name = 'book'
    login_url = 'login'
    permission_required = 'books.all_actions_book'


class BookSureDeleteView(TemplateView):
    template_name = "sure_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["book"] = Book.objects.filter(pk=self.kwargs['pk']).first()
        return context


