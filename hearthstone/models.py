from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from random import randint

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    credit = models.IntegerField(default=200)



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        card_counter = Card.objects.all().count()
        cards = []
        for i in range(30):
            random_index = randint(0, card_counter - 1)
            card = Card.objects.all()[random_index]
            cards.append(card)
            card_user = CardUser(card=card, user=instance)
            card_user.save()
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


class CardUser(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class CardDeck(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)

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
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Message(models.Model):
    content = models.CharField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    def __str__(self):
        return self.content
