# Generated by Django 5.0.3 on 2024-04-06 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_alter_book_genre_alter_borrowrequest_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
