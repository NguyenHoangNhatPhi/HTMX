# Generated by Django 5.0.6 on 2024-05-22 09:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("films", "0003_alter_film_options_userfilms"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="film",
            name="users",
        ),
        migrations.AddField(
            model_name="film",
            name="users",
            field=models.ManyToManyField(
                related_name="films",
                through="films.UserFilms",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]