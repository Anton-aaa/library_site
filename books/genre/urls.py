from django.urls import path
from books.genre.views import (GenreCreateView,
                               GenreListView,
                               GenreDeleteView,
                               GenreUpdateView
                              )


urlpatterns = [
    path("create/", GenreCreateView.as_view(), name="genre_create"),
    path("list/", GenreListView.as_view(), name="genre_list"),
    path('delete/<int:pk>/', GenreDeleteView.as_view(), name='genre_delete'),
    path('update/<int:pk>/', GenreUpdateView.as_view(), name='genre_update'),
]