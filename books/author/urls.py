from django.urls import path
from books.author.views import (AuthorCreateView,
                                AuthorListView,
                                AuthorDeleteView,
                                AuthorUpdateView,
                                AuthorDetailView
                              )

urlpatterns = [
    path("create/", AuthorCreateView.as_view(), name="author_create"),
    path("list/", AuthorListView.as_view(), name="author_list"),
    path('delete/<int:pk>/', AuthorDeleteView.as_view(), name='author_delete'),
    path('update/<int:pk>/', AuthorUpdateView.as_view(), name='author_update'),
    path("<int:pk>/", AuthorDetailView.as_view(), name='author_detail'),
]