from django.urls import path
from books.borrow.views import (BorrowRequestCreateView,
                                BorrowRequestSuccessView,
                                BorrowRequestListView,
                                BorrowRequestApproveView,
                                BorrowRequestRejectView,
                                BorrowRequestCompleteView,
                                BorrowRequestUserListView,
                                BorrowRequestTakeView,
                                BorrowRequestDetailView,
                                BorrowRequestDeadlineTrackingView
                              )

urlpatterns = [
    path("create/<int:pk>/", BorrowRequestCreateView.as_view(), name="borrow_create"),
    path("success/<int:pk>/", BorrowRequestSuccessView.as_view(), name="borrow_success"),
    path("list/", BorrowRequestListView.as_view(), name="borrow_list"),
    path("approve/<int:pk>", BorrowRequestApproveView.as_view(), name="borrow_approve"),
    path("reject/<int:pk>", BorrowRequestRejectView.as_view(), name="borrow_reject"),
    path("complete/<int:pk>", BorrowRequestCompleteView.as_view(), name="borrow_complete"),
    path("user_list/", BorrowRequestUserListView.as_view(), name="borrow_user_list"),
    path("take_book/<int:pk>", BorrowRequestTakeView.as_view(), name="borrow_take"),
    path("detail/<int:pk>", BorrowRequestDetailView.as_view(), name='borrow_detail'),
    path("deadline_tracking", BorrowRequestDeadlineTrackingView.as_view(), name='borrow_deadline_tracking'),
]