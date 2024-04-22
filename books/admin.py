from django.contrib import admin
from .models import (Genre,
                     Author,
                     Book,
                     BorrowRequest, NoticeBorrow
                     )
from django.forms import TextInput, Textarea
from django.db import models


class GenreAdmin(admin.ModelAdmin):
    field = ('name')
    list_display = ('id', 'name')

admin.site.register(Genre, GenreAdmin)

class AuthorAdmin(admin.ModelAdmin):
    fields = ('name', 'bio')
    list_display = ('id', 'name', 'bio')

admin.site.register(Author, AuthorAdmin)

class BookAdmin(admin.ModelAdmin):
    fields = ('title',
              'summary',
              'isbn',
              'available',
              'published_date',
              'publisher',
              'genre',
              'author',
              'borrower'
              )
    list_display = (
              'title',
              'id',
              'isbn',
              'available',
              'published_date',
              'publisher',
              )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }

admin.site.register(Book, BookAdmin)


class BorrowRequestAdmin(admin.ModelAdmin):
    fields = ('status',)
    list_display = ('book',
                    'id',
                    'borrower',
                    'status',
                    'overdue',
                    'request_date',
                    'approval_date',
                    'due_date',
                    'complete_date',
              )

admin.site.register(BorrowRequest, BorrowRequestAdmin)

class NoticeBorrowAdmin(admin.ModelAdmin):
    fields = ('borrow_result',)
    list_display = ('id',
              'borrow_request',
              'notice_date',
              'borrow_result',
              'refusal_message',
              'viewed',
              )

admin.site.register(NoticeBorrow, NoticeBorrowAdmin)