import datetime
from django.db.models import F
from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins
from books.filters import IsOwnerBorrowFilterBackend, IsRecipientFilterBackend
from books.forms import SearchForm
from books.models import NoticeBorrow, Book, Genre, BorrowRequest, User
from library.permissions import IsLibrarianOrAdmin, IsBorrowerOrAdminOrLibrarian, IsRecipientOrAdminOrLibrarian
from library.serializers import (GenreSerializer,
                                 BookSerializer,
                                 BorrowRequestSerializer,
                                 UserSerializer,
                                 NoticeBorrowSerializer)


class MainView(TemplateView):
    template_name = "main.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            not_read = NoticeBorrow.objects.filter(borrow_request__borrower=self.request.user, viewed=False).first()
            context['unread'] = not_read
        return context


def search_book(request):
    form = SearchForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            title = form.cleaned_data['title']
            all_books = Book.objects.filter(title__icontains=title)
            return render(request, 'search_book_result.html', {"books": all_books, "title":title})
        print(form)
    return render(request, 'search_book.html', {'form': form})


class GenreModelViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.action == "list":
            return [AllowAny()]

        return super().get_permissions()



class UserModelViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            return [IsLibrarianOrAdmin()]

        return super().get_permissions()


class BookModelViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsLibrarianOrAdmin]

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            return [AllowAny()]

        return super().get_permissions()


class BorrowRequestModelViewSet(mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.CreateModelMixin,
                           mixins.UpdateModelMixin,
                           GenericViewSet
                           ):
    queryset = BorrowRequest.objects.all()
    serializer_class = BorrowRequestSerializer
    permission_classes = [IsBorrowerOrAdminOrLibrarian]
    filter_backends = [IsOwnerBorrowFilterBackend]

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated()]

        if self.action == "list":
            return [IsBorrowerOrAdminOrLibrarian()]

        if self.action == "retrieve":
            return [IsBorrowerOrAdminOrLibrarian()]

        return super().get_permissions()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(borrower=user)

    def perform_update(self, serializer):

        borrow = self.get_object()
        book = borrow.book
        print(book.borrower)
        if serializer.validated_data['status'] == 2:
            book.available = False
            book.borrower = borrow.borrower
            book.save()
            serializer.save(approval_date=datetime.date.today())

        if serializer.validated_data['status'] == 4:
            book.available = True
            book.borrower = None
            book.save()
            serializer.save(complete_date=datetime.date.today())


        serializer.save()



class NoticeBorrowModelViewSet(mixins.ListModelMixin,
                           mixins.UpdateModelMixin,
                           GenericViewSet
                           ):
    queryset = NoticeBorrow.objects.all()
    serializer_class = NoticeBorrowSerializer
    permission_classes = [IsRecipientOrAdminOrLibrarian]
    filter_backends = [IsRecipientFilterBackend]



