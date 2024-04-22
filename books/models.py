from django.core.validators import MaxValueValidator
from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()

class Author(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField()

    class Meta:
        permissions = (
            ('all_actions_author', "Can create, update, delete author"),
        )

        ordering = ['name']


    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        permissions = (
            ('all_actions_genre', "Can create, update, delete genre"),
        )
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    summary = models.TextField()
    isbn = models.CharField(max_length=17, unique=True)
    available = models.BooleanField(default=True)
    published_date = models.PositiveIntegerField(
            validators=[
                MaxValueValidator(datetime.now().year)])
    publisher = models.CharField(max_length=255)
    genre = models.ManyToManyField(Genre, blank=True)
    author = models.ManyToManyField(Author)
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        permissions = (
            ('all_actions_book', "Can create, update, delete book"),
        )


    def __str__(self):
        return self.title


class BorrowRequest(models.Model):
    PENDING = 1
    APPROVED = 2
    COLLECTED = 3
    COMPLETE = 4
    DECLINED = 5
    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (APPROVED, "Approved"),
        (COLLECTED, "Collected"),
        (COMPLETE, "Complete"),
        (DECLINED, "Declined"),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING)
    overdue = models.BooleanField(default=False)
    request_date = models.DateField(auto_now_add=True)
    approval_date = models.DateField(null=True)
    due_date = models.DateField(null=True)
    complete_date = models.DateField(null=True)

    class Meta:
        permissions = (
            ('process_request', "Can confirm, reject, complete borrow request"),
        )
        ordering = ['-request_date']

class NoticeBorrow(models.Model):
    borrow_request = models.ForeignKey(BorrowRequest, on_delete=models.CASCADE)
    notice_date = models.DateField(auto_now_add=True)
    borrow_result = models.BooleanField()
    refusal_message = models.CharField(max_length=350, null=True, blank=True)
    viewed = models.BooleanField(default=False)

    class Meta:
        ordering = ['viewed', '-notice_date']
