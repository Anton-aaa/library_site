from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
import datetime
from books.models import Genre, Book, BorrowRequest, NoticeBorrow, User
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["name",]


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'is_staff',
            'password',
            'password2'
        ]

    extra_kwargs = {
        'first_name': {'required': True},
        'last_name': {'required': True}}

    def validate(self, data):
        super().validate(data)
        if data['password'] != data.pop('password2'):
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return data

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["title",
                  "summary",
                  "isbn",
                  "available",
                  "published_date",
                  "publisher",
                  "genre",
                  "author",
                  "borrower",
                  ]
        read_only_fields = ['borrower',]


class BorrowRequestSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(many=False, required=False, queryset=Book.objects.all())
    rejection_reason = serializers.CharField(max_length=350, write_only=True, required=False)
    class Meta:
        model = BorrowRequest
        fields = ["id",
                  "book",
                  "borrower",
                  "status",
                  "overdue",
                  "request_date",
                  "approval_date",
                  "due_date",
                  "complete_date",
                  "rejection_reason"
                  ]
        read_only_fields = ['borrower',
                            'overdue',
                            'approval_date',
                            'complete_date']

    def validate(self, data):
        super().validate(data)
        user = self.context['request'].user

        if not data.get('status'):
            raise serializers.ValidationError("'Status' can't be empty")

        if self.context['request'].method == 'POST':
            book = Book.objects.filter(pk=data['book'].id).first()
            old_borrow = BorrowRequest.objects.filter(book=book, borrower=user)

            if not data['status'] == 1:
                raise serializers.ValidationError("Status must be 'Pending'")
            if (data.get('rejection_reason')):
                raise serializers.ValidationError("Rejection reason must not be")
            if (data.get('due_date')):
                raise serializers.ValidationError("Due date must not be")

            # does the user have a borrow request for this book?
            for borrow in old_borrow:
                if borrow.status == 1 or borrow.status == 2 or borrow.status == 3:
                    raise serializers.ValidationError("User already has active borrow request for this book")

        if self.context['request'].method == 'PUT' or self.context['request'].method == 'PATCH':
            borrow = self.instance

            # ordinary user can only change the status to 3:'Collected'
            if not (user.is_staff or user.groups.filter(name='librarians').exists()) and not data['status'] == 3:
                raise serializers.ValidationError("User can only change status to 'Collected'")

            if (not borrow.borrower == user and user.is_staff or user.groups.filter(name='librarians').exists() and
            data['status'] == 3):
                raise serializers.ValidationError("Librarians cannot collect books based on other people's requests.")

            # restrictions for librarians
            if data.get('book'):
                raise serializers.ValidationError("Book not subject to change")
            if data.get('rejection_reason') and not data['status'] == 5:
                raise serializers.ValidationError("Rejection reason must be indicated along with the status 'Declined'")

            # create a refusal with the reason for the refusal
            if data.get('rejection_reason'):
                message = data.pop('rejection_reason')
                NoticeBorrow.objects.create(borrow_request=borrow, borrow_result=False, refusal_message=message)

            # create a note about the acceptance of the application
            if data['status'] == 2:
                NoticeBorrow.objects.create(borrow_request=borrow, borrow_result=True)

            if data.get('due_date') and not data['status'] == 2:
                raise serializers.ValidationError("Due date not subject to change")
            if data.get('due_date') and data['due_date'] <= datetime.date.today():
                raise serializers.ValidationError("Due date shouldn't be today or earlier")
            if data['status'] == 1:
                raise serializers.ValidationError("You can't change the status to 'Pending'")
            if data['status'] == 2 and not data.get('due_date'):
                raise serializers.ValidationError("Due date сan't be empty")
            if borrow.status == 1 and not (data['status'] == 2 or data['status'] == 5):
                raise serializers.ValidationError("Status must be 'Approved' or 'Declined'")
            if borrow.status == 2 and not (data['status'] == 3 or data['status'] == 4):
                raise serializers.ValidationError("Status must be 'Collected' or 'Complete'")
            if borrow.status == 3 and not (data['status'] == 4):
                raise serializers.ValidationError("Status must be 'Complete'")
            if borrow.status == 4:
                raise serializers.ValidationError("Status 'Complete' not subject to change")
            if borrow.status == 5:
                raise serializers.ValidationError("Status 'Declined' not subject to change")
        return data


class NoticeBorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoticeBorrow
        fields = ["borrow_request",
                  "notice_date",
                  "borrow_result",
                  "refusal_message",
                  "viewed",
                  ]
        read_only_fields = ['borrow_request',
                            'notice_date',
                            'borrow_result',
                            'refusal_message']
