# Generated by Django 2.2.dev20181221175106 on 2019-01-05 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hearthstone', '0003_battle'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='elo',
            field=models.IntegerField(default=1400),
        ),
    ]