from random import randint
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import UserRegisterForm
from django.contrib import messages
from .models import Card, Deck, Game, CardUser, CardDeck
import json


def home(request):
    #TODO Redirect if connected
    title = 'Accueil'
    slugs = [
        'test',
        'tast',
        'tost',
    ]
    context = {
        'title': title,
        'games': Game.objects.all(),
        'cards': Card.objects.all(),
        'slugs': slugs,
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
    return render(request, 'hearthstone/game.html')


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
    deck = Deck(id=deck_id)
    cards = {}
    cardsInDeck = CardDeck.objects.all().filter(deck_id=deck_id)
    for cardInDeck in cardsInDeck:
        card = Card(id=cardInDeck.card_id)
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
            deck = Deck(title="test", user=request.user)
            deck.save()
            json_data = json.loads(request.body)
            cards = json_data['deck']
            #TODO Check disponibility
            for card in cards:
                for x in range(card['count']):
                    card2add = Card(id=card['id'])
                    cardDeck = CardDeck(card=card2add, deck=deck)
                    cardDeck.save()
            return JsonResponse("Saved", safe=False)

# elif request.user.is_authenticated and request.user.profile.credit < 100:
#     messages.warning(request, f'Vous n\'avez pas assez de crédit :(')
#     return redirect('home')
# else:
#     messages.warning(request, f'Vous devez être connecté pour accéder à cette page')
#     return redirect('home')
