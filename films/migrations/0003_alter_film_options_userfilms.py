# Generated by Django 5.0.6 on 2024-05-22 09:19

import django.db.models.deletion
import django.db.models.functions.text
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0002_film'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='film',
            options={'ordering': [django.db.models.functions.text.Lower('name')]},
        ),
        migrations.CreateModel(
            name='UserFilms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveSmallIntegerField()),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='films.film')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]
