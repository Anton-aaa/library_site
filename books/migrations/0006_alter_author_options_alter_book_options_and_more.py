# Generated by Django 5.0.3 on 2024-04-08 19:08

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_alter_author_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='book',
            options={'permissions': (('all_actions_book', 'Can create, update, delete book'),)},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ['name']},
        ),
        migrations.AlterField(
            model_name='book',
            name='borrower',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.ManyToManyField(blank=True, to='books.genre'),
        ),
        migrations.AlterField(
            model_name='book',
            name='published_date',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(2024)]),
        ),
    ]
