from django.urls import path
from books.notice_borrow.views import (NoticeBorrowUserListView,
                                       NoticeBorrowUserReadView
                                      )

urlpatterns = [
    path("list/", NoticeBorrowUserListView.as_view(), name="notice_borrow_list"),
    path("all_read/", NoticeBorrowUserReadView.as_view(), name="notice_borrow_all_read"),
]