# Generated by Django 5.0.3 on 2024-04-07 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_alter_genre_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'permissions': (('all_actions_author', 'Can create, update, delete author'),)},
        ),
    ]