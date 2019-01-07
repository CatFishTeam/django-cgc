# Generated by Django 2.2.dev20190107071306 on 2019-01-07 08:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hearthstone', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='user',
        ),
        migrations.AddField(
            model_name='card',
            name='owner',
            field=models.ManyToManyField(related_name='cards', to=settings.AUTH_USER_MODEL),
        ),
    ]
