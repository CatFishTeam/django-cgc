# Generated by Django 2.2.dev20190107212229 on 2019-01-07 23:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hearthstone', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cardsuser',
            old_name='count',
            new_name='quantity',
        ),
    ]
