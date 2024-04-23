from django.contrib import admin
from django.urls import path, include

from books.views import (MainView,
                         search_book,
                         GenreModelViewSet,
                         BookModelViewSet,
                         BorrowRequestModelViewSet,
                         UserModelViewSet,
                         NoticeBorrowModelViewSet
                         )
from rest_framework.authtoken import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register("genre", GenreModelViewSet)
router.register("book", BookModelViewSet)
router.register("borrow", BorrowRequestModelViewSet)
router.register("profile", UserModelViewSet)
router.register("notice_borrow", NoticeBorrowModelViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path("", MainView.as_view(), name='main'),
    path('search', search_book, name='search'),
    path('profile/', include("books.profile.urls")),
    path('genre/', include("books.genre.urls")),
    path('author/', include("books.author.urls")),
    path('book/', include("books.book.urls")),
    path('borrow/', include("books.borrow.urls")),
    path('notice_borrow/', include("books.notice_borrow.urls")),
    path('api-token-auth/', views.obtain_auth_token),
]
