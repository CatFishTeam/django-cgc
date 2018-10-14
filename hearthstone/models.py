from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    credit = models.IntegerField(default=200)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Deck(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Card(models.Model):
    title = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, null=True, blank=True)


@receiver(pre_save, sender=Card)
def slugify(sender, instance, *args, **kwargs):
    instance.slug = instance.title.replace(' ', '_').replace('\'', '_')


class Card_Deck(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)

    def __str__(self):
        return self.card.title


class Game(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player_one')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player_two')
    winner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.winner.username
