from random import randint
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import UserRegisterForm, TopicCreationForm, MessageCreationForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .models import Card, Deck, Game, CardUser, CardDeck, Topic, Message, User, Battle
from django.db.models import Count
import json
import requests


def home(request):
    #TODO Redirect if connected
    title = 'Accueil'
    slugs = [
        'test',
        'tast',
        'tost',
    ]

    #  Get all cards from Mashable Hearthstone API
    url = 'https://omgvamp-hearthstone-v1.p.mashape.com/cards?locale=frFR'
    headers = {"X-Mashape-Key": "XTUi1bdLD6mshqZg64hA0G1f5c5xp1VB2XxjsntfVEFVdnzQ25"}

    # r = requests.get(url, headers=headers)
    # cardsJson = r.json()
    # cardsText = r.text

    context = {
        'title': title,
        'games': Game.objects.all()[:15],
        'cards': Card.objects.all()[:8],
        'slugs': slugs
    }

    return render(request, 'hearthstone/index.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Le compte de {username} a bien été créé !')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def game(request):
    decks = Deck.objects.all().filter(user_id=request.user.id)
    return render(request, 'hearthstone/game.html', {'decks': decks})

def launchGame(request, deck_id):
    if request.user.is_authenticated:
        deck_played = Deck.objects.get(id=deck_id)
        cards_played = CardDeck.objects.filter(deck_id=deck_played.id)

        decks = Deck.objects.exclude(user_id=request.user.id)
        contender_deck = decks[randint(0, decks.count() - 1)] #Choose a random contender
        contender = User.objects.get(id=contender_deck.user_id)

        contender_cards = CardDeck.objects.filter(deck_id=contender_deck.id)

#        player1_hp = 30
#        player2_hp = 30

#
#        for card_1 in cards_played:
#            for card_2 in contender_cards:
#                dmg = card_1.attack - card_2.attack
#                if dmg > 0 :
#
#                if player1_hp <= 0:

        battle = Battle(player1_id=request.user.id, player2_id=contender.id, result=randint(-1, 1), round=randint(15, 30))
        battle.save()


        #import pdb; pdb.set_trace()


        return render(request, 'hearthstone/launchGame.html', {'conteder': contender, 'battle': battle})
    else:
        messages.warning(request, f'Vous devez être connecté pour accéder à cette page')
        return redirect('home')

def card(request, card_id):
    card = get_object_or_404(Card, pk=card_id)
    return render(request, 'hearthstone/card.html', {'card': card})


def buyCards(request):
    cardCounter = Card.objects.all().count()
    cards = []
    if request.user.is_authenticated and request.user.profile.credit >= 100:
        for i in range(8):
            random_index = randint(0, cardCounter - 1)
            card = Card.objects.all()[random_index]
            cards.append(card)
            cardUser = CardUser(card=card, user=request.user)
            cardUser.save()
        request.user.profile.credit -= 100
        request.user.save()
    elif request.user.is_authenticated and request.user.profile.credit < 100:
        messages.warning(request, f'Vous n\'avez pas assez de crédit :(')
        return redirect('home')
    else:
        messages.warning(request, f'Vous devez être connecté pour accéder à cette page')
        return redirect('home')

    return render(request, 'hearthstone/buy-cards.html', {'cards': cards})


def myCards(request):
    cardsUser = CardUser.objects.all().filter(user_id=request.user.id)
    cards = []

    for cardUser in cardsUser:
        card = cardUser.card
        cards.append(card)

    return render(request, 'hearthstone/my-cards.html', {'cards': cards})


def myDecks(request):
    decks = Deck.objects.all().filter(user_id=request.user.id)
    return render(request, 'hearthstone/my-decks.html', {'decks': decks})

def showDeck(request, deck_id):
    deck = Deck.objects.get(id=deck_id)
    print(deck)
    cards = []
    cardsInDeck = CardDeck.objects.all().filter(deck_id=deck_id)
    for cardInDeck in cardsInDeck:
        card = cardInDeck.card
        cards.append(card)
    return render(request, 'hearthstone/show-deck.html', {'cards': cards, 'deck': deck})

    #for cardInDeck in cardsInDeck:
    #    if cardInDeck in cards:
    #        cards[cardInDeck] += 1
    #    else:
    #        cards[cardInDeck] = 1

def deleteDeck(request, deck):
    Deck(id=deck).delete()
    messages.success(request, f'Votre deck a bien été supprimé :) ')
    return redirect('myDecks')


def createDeck(request):
    cardsUser = CardUser.objects.all().filter(user_id=request.user.id)
    cards = {}
    for cardUser in cardsUser:
        card = cardUser.card
        if card in cards:
            cards[card] += 1
        else:
            cards[card] = 1
    return render(request, 'hearthstone/create-deck.html', {'cards': cards})

def saveDeck(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            json_data = json.loads(request.body)
            title = json_data['title']
            cards = json_data['deck']

            deck = Deck(title=title, user=request.user)
            deck.save()

            #TODO Check disponibility
            for card in cards:
                for x in range(card['count']):
                    card2add = Card(id=card['id'])
                    cardDeck = CardDeck(card=card2add, deck=deck)
                    cardDeck.save()
            return JsonResponse(deck.id, safe=False)

# elif request.user.is_authenticated and request.user.profile.credit < 100:
#     messages.warning(request, f'Vous n\'avez pas assez de crédit :(')
#     return redirect('home')
# else:
#     messages.warning(request, f'Vous devez être connecté pour accéder à cette page')
#     return redirect('home')

def forum(request):
    topics = Topic.objects.order_by('-created_at').annotate(number_of_messages=Count('message'))

    context = {
        'topics': topics,
    }

    return render(request, 'forum/index.html', context)

def createTopic(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TopicCreationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            topic = form.save(commit=False)
            topic.author = request.user
            topic.save()
            messages.success(request, f'Votre sujet a bien été créé !')
            return redirect('topic', topic_id=topic.id)
    else:
        form = TopicCreationForm()
    return render(request, 'forum/create.html', {'form': form})


def topic(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = MessageCreationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.author = request.user
            new_message.topic = topic
            new_message.save()
            messages.success(request, f'Votre message a bien été ajouté au sujet !')
    else:
        form = MessageCreationForm()

    msgs = Message.objects.all().filter(topic=topic)

    context = {
        'topic': topic,
        'msgs': msgs,
        'form': form,
    }

    return render(request, 'forum/topic.html', context)

def profile(request):
    return render(request, 'hearthstone/profile.html', {})

def changePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Votre mot de passe a bien été changé !')
            return redirect('changePassword')
        else:
            messages.error(request, 'Merci de corriger les erreurs ci-dessous')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change-password.html', {
        'form': form
    })
