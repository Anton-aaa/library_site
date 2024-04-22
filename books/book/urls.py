from django.urls import path
from books.book.views import (BookCreateView,
                              BookListView,
                              BookDetailView,
                              BookDeleteView,
                              BookUpdateView,
                              BookSureDeleteView
                              )

urlpatterns = [
    path("create/", BookCreateView.as_view(), name="book_create"),
    path("list/", BookListView.as_view(), name="book_list"),
    path("detail/<int:pk>/", BookDetailView.as_view(), name='book_detail'),
    path('delete/<int:pk>/', BookDeleteView.as_view(), name='book_delete'),
    path('update/<int:pk>/', BookUpdateView.as_view(), name='book_update'),
    path("sure_delete/<int:pk>/", BookSureDeleteView.as_view(), name='book_sure_delete'),
]