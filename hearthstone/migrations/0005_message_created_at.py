# Generated by Django 2.2.dev20190105174938 on 2019-01-05 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hearthstone', '0004_profile_elo'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
