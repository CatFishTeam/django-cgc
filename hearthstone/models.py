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
        activity = Activity(
            author=instance,
            content=instance.username + " a rejoint Hearthstone !",
            type="register")
        activity.save()
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
    owner = models.ManyToManyField(User, related_name="cards")

    def __str__(self):
        return self.title


@receiver(pre_save, sender=Card)
def slugify(sender, instance, *args, **kwargs):
    instance.slug = instance.title \
        .replace(' ', '_') \
        .replace('\'', '_') \
        .replace(',', '_') \
        .replace('!', '_') \
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


class Activity(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    content = models.CharField(max_length=2000)
    type = models.CharField(max_length=150)
    related_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.content


class Subscribe(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower_user')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed_user')


@receiver(post_save, sender=Subscribe)
def save_subscribe_activity(sender, instance, created, **kwargs):
    if created:
        activity = Activity(
            author=instance.follower,
            content=instance.follower.username + " suit maintenant " + instance.followed.username,
            type="follow",
            related_user=instance.followed)
        activity.save()


class Topic(models.Model):
    title = models.CharField(max_length=150)
    content = models.CharField(max_length=2000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.title


@receiver(post_save, sender=Topic)
def save_topic_activity(sender, instance, created, **kwargs):
    if created:
        activity = Activity(
            author=instance.author,
            content=instance.author.username + " a créé un sujet sur le forum : " + instance.title,
            type="forum")
        activity.save()


class Message(models.Model):
    content = models.CharField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.content


@receiver(post_save, sender=Message)
def save_message_activity(sender, instance, created, **kwargs):
    if created:
        activity = Activity(
            author=instance.author,
            content=instance.author.username + " a répondu sur un sujet du forum : " + instance.topic.title,
            type="forum")
        activity.save()


class Battle(models.Model):
    player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_1_provider_profile')
    player2 = models.ForeignKey(User,  on_delete=models.CASCADE, related_name='user_2_provider_profile')
    round = models.IntegerField(null=False, blank=True)
    result = models.IntegerField(null=False, blank=True) # 1 player1 | 0 null | -1 player2


@receiver(post_save, sender=Battle)
def save_battle_activity(sender, instance, created, **kwargs):
    if created:
        activity = Activity(
            author=instance.player1,
            content=instance.player1 + " a joué contre " + instance.player2,
            type="game",
            related_user=instance.player2)
        activity.save()
