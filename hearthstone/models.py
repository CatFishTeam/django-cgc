from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from random import randint

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    credit = models.IntegerField(default=200)
    elo = models.IntegerField(default=1400)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.save()


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
    img = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    cost = models.IntegerField(null=True, blank=True)
    health = models.IntegerField(null=True, blank=True)
    attack = models.IntegerField(null=True, blank=True)
    deck = models.ForeignKey(Deck, on_delete=models.PROTECT, null=True)
    user = models.ManyToManyField(User)

    def __str__(self):
        return self.title


@receiver(pre_save, sender=Card)
def slugify(sender, instance, *args, **kwargs):
    instance.slug = instance.title\
        .replace(' ', '_')\
        .replace('\'', '_')\
        .replace(',', '_')\
        .replace('!', '_')\
        .replace('-', '_')
    instance.slug = instance.slug.replace('__', '_')
    instance.slug = instance.slug.rstrip('_')


class Game(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player_one')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player_two')
    winner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.winner.username


class Topic(models.Model):
    title = models.CharField(max_length=150)
    content = models.CharField(max_length=2000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.title


class Message(models.Model):
    content = models.CharField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class Battle(models.Model):
    player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_1_provider_profile')
    player2 = models.ForeignKey(User,  on_delete=models.CASCADE, related_name='user_2_provider_profile')
    round = models.IntegerField(null=False, blank=True)
    result = models.IntegerField(null=False, blank=True) # 1 player1 | 0 null | -1 player2
