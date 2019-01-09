from random import randint
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import UserRegisterForm, TopicCreationForm, MessageCreationForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Count, Q
from django.core.paginator import Paginator
from .models import Profile, Card, Deck, CardsUser, CardsDeck, Topic, Message, User, Battle, Activity
import random
import json

# import pdb; pdb.set_trace()

#  Get all cards from Mashable Hearthstone API
#url = 'https://omgvamp-hearthstone-v1.p.mashape.com/cards?locale=frFR'
#headers = {"X-Mashape-Key": "XTUi1bdLD6mshqZg64hA0G1f5c5xp1VB2XxjsntfVEFVdnzQ25"}

# r = requests.get(url, headers=headers)
# cardsJson = r.json()
# cardsText = r.text


def home(request):
    # TODO Redirect if connected
    if request.user.is_authenticated:
        if request.user.cards.count() == 0:
            return render(request, 'hearthstone/first_visit.html')
    title = 'Accueil'
    slugs = [
        'test',
        'tast',
        'tost',
    ]

    cards = []
    allCards = Card.objects.all()
    for i in range(0, 8):
        card = Card.objects.all()[randint(0, allCards.count() - 1)]
        cards.append(card)

    context = {
        'title': title,
        'battles': Battle.objects.all()[:15],
        'cards': cards,
        'slugs': slugs
    }


    return render(request, 'hearthstone/index.html', context)


def open_first_deck(request):
    if request.user.is_authenticated:
        if request.user.cards.count() == 0:
            number_of_card = Card.objects.exclude(type="Hero Power").count()
            for i in range(30):
                random_card = Card.objects.exclude(type="Hero Power")[randint(0, number_of_card - 1)]
                card, created = CardsUser.objects.get_or_create(user=request.user, card=random_card, defaults={'quantity': 1})
                if created:
                    card.save()
                else:
                    card.quantity += 1
                    card.save()

            return render(request, 'hearthstone/first_opening.html')
        else:
            messages.warning(request, f'Vous avez tenté de tricher !')
            return render(request, 'hearthstoneindex.html')


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



def launch_game(request, deck_id):
    if request.user.is_authenticated:

        opponent_deck = Deck.objects.all().exclude(user_id=request.user.id)
        opponent_deck = opponent_deck[random.randint(0, opponent_deck.count() - 1)]

        opponent = User.objects.get(pk=opponent_deck.user_id)

        player_cards = CardsDeck.objects.all().filter(deck_id=deck_id)
        player_deck = []
        for player_card in player_cards:
            for i in range(player_card.quantity):
                player_deck.append(player_card)

        opponent_cards = CardsDeck.objects.all().filter(deck_id=opponent_deck.id)
        opponent_deck = []
        for opponent_card in opponent_cards:
            for i in range(opponent_card.quantity):
                opponent_deck.append(opponent_card)

        player_hp = 30
        opponent_hp = 30
        turn = 0

        while player_hp and opponent_hp >= 0:
            turn += 1
            player_card = player_deck.pop(randint(0, len(player_deck) - 1))
            opponent_card = opponent_deck.pop(randint(0, len(opponent_deck) - 1))

            if player_card.card.type == 'Spell':
                opponent_hp -= player_card.card.cost if player_card.card.cost is not None else 0
            if player_card.card.type == 'Weapon':
                continue
            if player_card.card.type == "Minion":
                if opponent_card.card.type == "Minion":
                    dmg = opponent_card.card.attack if opponent_card.card.attack is not None else 0 - player_card.card.attack if player_card.card.attack is not None else 0
                    if dmg >= 0:
                        opponent_hp -= dmg
                    else:
                        player_hp -= dmg
                if opponent_card.card.type == "Spell":
                    player_hp -= opponent_card.card.cost if opponent_card.card.cost is not None else 0
                if opponent_card.card.type == "Weapon":
                    opponent_hp -= player_card.card.attack if player_card.card.attack is not None else 0

        result = 1 if player_hp > opponent_hp else -1
        battle = Battle.objects.create(player=request.user, opponent=opponent, result=result, round=turn)
        return render(request, 'hearthstone/launchGame.html', {'battle': battle})
    else:
        messages.warning(request, f'Vous devez être connecté pour accéder à cette page')
        return redirect('home')


def battle(request, battle_id):
    battle = Battle.objects.get(pk=battle_id)
    return render(request, 'hearthstone/game.html', {'battle': battle})


def game(request):
    return render(request, 'hearthstone/game.html')


def card(request, card_id):
    card = get_object_or_404(Card, pk=card_id)
    return render(request, 'hearthstone/card.html', {'card': card})


def buy_cards(request):
    card_counter = Card.objects.all().filter(~Q(type="Hero Power")).count()
    cards = []
    credit = request.user.profile.credit
    if request.user.is_authenticated and credit >= 100:
        for i in range(8):
            random_index = randint(0, card_counter - 1)
            random_card = Card.objects.all().filter(~Q(type="Hero Power"))[random_index]
            card, created = CardsUser.objects.get_or_create(user=request.user, card=random_card, defaults={'quantity': 1})
            if created:
                card.save()
            else:
                card.quantity += 1
                card.save()
            cards.append(random_card)
        credit -= 100
        request.user.profile.credit = credit
        request.user.save()
    elif request.user.is_authenticated and credit < 100:
        messages.warning(request, f'Vous n\'avez pas assez de crédit :(')
        return redirect('home')
    else:
        messages.warning(request, f'Vous devez être connecté pour accéder à cette page')
        return redirect('home')
    return render(request, 'hearthstone/buy-cards.html', {'cards': cards, 'credit': credit})


def my_cards(request):
    profile = get_object_or_404(Profile, pk=request.user.id)
    credit = request.user.profile.credit
    return render(request, 'hearthstone/my-cards.html', {'credit': credit, 'profile': profile})


def my_decks(request):
    decks = Deck.objects.all().filter(user_id=request.user.id)
    return render(request, 'hearthstone/my-decks.html', {'decks': decks})


def show_deck(request, deck_id):
    deck = Deck.objects.get(id=deck_id)
    return render(request, 'hearthstone/show-deck.html', {'deck': deck})


def delete_deck(request, deck):
    Deck(id=deck).delete()
    messages.success(request, f'Votre deck a bien été supprimé :) ')
    return redirect('myDecks')


def create_deck(request):
    return render(request, 'hearthstone/create-deck.html')


def save_deck(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            json_data = json.loads(request.body)
            title = json_data['title']
            cards = json_data['deck']

            deck = Deck(title=title, user=request.user)
            deck.save()

            # TODO Check disponibility
            for card in cards:
                card2add = Card(id=card['id'])
                cards_deck = CardsDeck(card=card2add, deck=deck, quantity=card['count'])
                cards_deck.save()
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


def create_topic(request):
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


def user(request, user_id):
    profile = get_object_or_404(Profile, pk=user_id)

    context = {
        'profile': profile
    }

    return render(request, 'hearthstone/user.html', context)


def change_password(request):
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


def community(request):
    profiles = Profile.objects.all()
    users = []
    for profile in profiles:
        user = {
            'profile': profile,
            'user': profile.user
        }
        users.append(user)
    context = {
        'users': users
    }
    return render(request, 'hearthstone/community.html', context)


def activities(request):
    activities = Activity.objects.all().order_by('-id').filter(Q(author=request.user.id) | Q(related_user=request.user.id))
    context = {
        'activities': activities
    }
    return render(request, 'hearthstone/activities.html', context)


def ladder(request):
    users = User.objects.all()
    paginator = Paginator(users, 2)

    page = request.GET.get('page')
    users = paginator.get_page(page)

    return render(request, 'hearthstone/ladder.html', {'users': users})
