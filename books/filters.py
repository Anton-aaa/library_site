from rest_framework import filters


class IsOwnerBorrowFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if request.user.is_staff or request.user.groups.filter(name='librarians').exists():
            return queryset.filter()

        return queryset.filter(borrower=request.user)