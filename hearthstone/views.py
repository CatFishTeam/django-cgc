from random import randint
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import UserRegisterForm, TopicCreationForm, MessageCreationForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, authenticate, logout, login
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Count, Q
from django.core.paginator import Paginator
from .models import Profile, Card, Deck, CardsUser, CardsDeck, Topic, Message, User, Battle, Activity, Subscribe, Exchange
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
        'battles': Battle.objects.order_by('-date')[:5],
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
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User.objects.create_user(username, username, password)
            login(request, user)
            messages.success(request, f'<b>{username}</b><br>  Votre compte a bien été créé !')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})



def launch_game(request, deck_id):
    if request.user.is_authenticated:

        opponent_deck = Deck.objects.all().exclude(user_id=request.user.id)

        if opponent_deck.exists():
            opponent_deck = opponent_deck[randint(0, opponent_deck.count() - 1)]

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
            actions = []

            while player_hp and opponent_hp >= 0:
                turn += 1
                player_card = player_deck.pop(randint(0, len(player_deck) - 1))
                #actions.append({player_card.card.img:request.user.username + " a joué la carte " + player_card.card.title})
                #actions.append({opponent_card.card.img:opponent.username + " a joué la carte " + opponent_card.card.title})
                opponent_card = opponent_deck.pop(randint(0, len(opponent_deck) - 1))
                if player_card.card.type == 'Spell':
                    dmg = player_card.card.cost if player_card.card.cost is not None else 0
                    opponent_hp -= dmg
                    actions.append({player_card.card.img:" Carte Sort jouée"})
                    actions.append({player_card.card.img:" Le jouueur : " + opponent.username + " n'a pas le temps de se défendre et perd " + str(dmg) + " points de vie"})
                if player_card.card.type == 'Weapon':
                    actions.append({player_card.card.img:"Carte Arme jouée"})
                    if opponent_card.card.type == "Minion":
                        dmg = opponent_card.card.attack if opponent_card.card.attack is not None else 0
                        actions.append({opponent_card.card.img:" Carte Minion : " + request.user.username + " a perdu " + str(dmg) + " points de vie"})
                        player_hp -= dmg
                    else:
                        dmg = opponent_card.card.cost if opponent_card.card.cost is not None else 0
                        actions.append({opponent_card.card.img:" Carte jouée : " + request.user.username + " a perdu " + str(dmg) + " points de vie"})
                        player_hp -= dmg
                if player_card.card.type == "Minion":
                    actions.append({player_card.card.img:" Carte Minion jouée"})
                    if opponent_card.card.type == "Minion":
                        dmg = opponent_card.card.attack if opponent_card.card.attack is not None else 0 - player_card.card.attack if player_card.card.attack is not None else 0
                        if dmg >= 0:
                            opponent_hp -= dmg
                            actions.append({player_card.card.img:"Carte Minion : " + opponent.username + " a perdu " + str(dmg) + " points de vie"})
                        else:
                            player_hp -= dmg
                            actions.append({opponent_card.card.img:"Carte Minion : " + request.user.username + " a perdu " + str(dmg) + " points de vie"})
                    if opponent_card.card.type == "Spell":
                        dmg = opponent_card.card.cost if opponent_card.card.cost is not None else 0
                        player_hp -= dmg
                        actions.append({opponent_card.card.img:"Carte Sort : " + opponent.username + " a perdu " + str(dmg) + " points de vie"})
                    if opponent_card.card.type == "Weapon":
                        dmg = player_card.card.attack if player_card.card.attack is not None else 0
                        opponent_hp -= dmg
                        actions.append({player_card.card.img:"Carte Arme : " + opponent.username + " a perdu " + str(dmg) + " points de vie"})

            randelo = randint(1, 10)
            if player_hp > opponent_hp:
                result = 1
                request.user.profile.elo += randelo
                request.user.profile.credit += 50
                opponent.profile.elo -= randelo
                request.user.profile.save()
                opponent.profile.save()
            else:
                result = -1
                request.user.profile.elo -= randelo
                opponent.profile.elo += randelo
                request.user.profile.save()
                opponent.profile.save()
            battle = Battle.objects.create(player=request.user, opponent=opponent, result=result, round=turn)
            return render(request, 'hearthstone/launchGame.html', {'battle': battle, 'actions': actions, 'player_hp': player_hp, 'opponent_hp': opponent_hp})
        else:
            messages.error(request, f"Il n'y a pas assez de decks pour faire une partie")
            return redirect('home')
    else:
        messages.warning(request, f'Vous devez être connecté pour accéder à cette page')
        return redirect('home')


def battle(request, battle_id):
    battle = Battle.objects.get(pk=battle_id)
    return render(request, 'hearthstone/battle.html', {'battle': battle})


def game(request):
    decks = Deck.objects.all().filter(user_id=request.user.id)
    return render(request, 'hearthstone/game.html',  {'decks': decks})


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
    profile = get_object_or_404(Profile, pk=request.user.id)
    exchanges = Exchange.objects.all().order_by('-id').filter(Q(user1=request.user.id) | Q(user2=request.user.id))
    battles = Battle.objects.all().order_by('-id').filter(Q(player=request.user.id) | Q(opponent=request.user.id))
    context = {
        'profile': profile,
        'exchanges': exchanges,
        'battles': battles
    }

    return render(request, 'hearthstone/profile.html', context)


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
    subscribes = Subscribe.objects.all().filter(follower_id=request.user.id)
    followed_users = []
    for subscribe in subscribes:
        followed_users.append(subscribe.followed)
    users = []
    for profile in profiles:
        user = {
            'profile': profile,
            'user': profile.user
        }
        users.append(user)
    context = {
        'users': users,
        'followed_users': followed_users
    }
    return render(request, 'hearthstone/community.html', context)


def activities(request):
    all_activities = []
    activities = Activity.objects.all().order_by('-id').filter(Q(author=request.user.id) | Q(related_user=request.user.id))
    for activity in activities:
        all_activities.append(activity)
    subscribes = Subscribe.objects.all().filter(follower_id=request.user.id)
    for subscribe in subscribes:
        friends_activities = Activity.objects.all().order_by('-id').filter(Q(author=subscribe.followed) | Q(related_user=subscribe.followed))
        for friends_activity in friends_activities:
            if friends_activity not in all_activities:
                all_activities.append(friends_activity)

    context = {
        'activities': all_activities
    }
    return render(request, 'hearthstone/activities.html', context)


def ladder(request):
    users = Profile.objects.all().order_by('elo').reverse()
    paginator = Paginator(users, 2)

    page = request.GET.get('page')
    users = paginator.get_page(page)

    return render(request, 'hearthstone/ladder.html', {'users': users})


def subscribe(request, user_id):
    followed_user = get_object_or_404(Profile, pk=user_id)

    subscribe, created = Subscribe.objects.get_or_create(follower=request.user, followed=followed_user.user)

    if created:
        messages.success(request, f'Vous êtes maintenant abonné à {followed_user.user.username}')
    else:
        messages.warning(request, f'Vous êtes déjà abonné à {followed_user.user.username}')

    subscribe.save()

    context = {
        'followed_user': followed_user
    }

    return render(request, 'hearthstone/subscribe.html', context)


# Echange : page pour le user1 de choisir une carte pour l'échange
def exchange(request, card_id):
    card = get_object_or_404(Card, pk=card_id)
    profiles = Profile.objects.all()
    context = {
        'card': card,
        'profiles': profiles
    }
    return render(request, 'hearthstone/exchange.html', context)


# Echange : le user1 a envoyé sa proposition d'échange au user2
def start_exchange(request):
    card = get_object_or_404(Card, pk=request.POST['card_id'])
    exchange_starter = request.user
    exchange_receiver = get_object_or_404(User, pk=request.POST['user_id'])

    exchange = Exchange.objects.create(user1=exchange_starter, user2=exchange_receiver, card1=card)

    messages.success(request, f"Votre demande d\'échange a bien été envoyée<br><a style='text-decoration: underline;' href='/exchange_status/{exchange.id}'>Voir l'échange</a>")
    return redirect('myCards')


# Echange : le user2 a soumis sa proposition
def continue_exchange(request):
    exchange = get_object_or_404(Exchange, pk=request.POST['exchange_id'])
    card = get_object_or_404(Card, pk=request.POST['card_id'])
    exchange.card2 = card
    exchange.save()

    messages.success(request, f"Votre proposition a bien été soumise")
    return redirect('exchange_status', exchange_id=exchange.id)


# Echange : user1 ou 2 a validé l'échange
def validate_exchange(request, exchange_id):
    exchange = get_object_or_404(Exchange, pk=exchange_id)

    if request.user == exchange.user1:
        exchange.user1_response = "OK"
        exchange.save()
        messages.success(request, f"Vous avez bien validé cet échange")
    elif request.user == exchange.user2:
        exchange.user2_response = "OK"
        exchange.save()
        messages.success(request, f"Vous avez bien validé cet échange")
    else:
        messages.error(request, f"Vous n'êtes pas autorisé à valider cet échange")

    # Accepté : on procède à l'échange des cartes entre joueurs
    if exchange.user1_response == 'OK' and exchange.user2_response == 'OK':
        exchange.status = 'Accepté'
        exchange.save()
        messages.success(request, f"L'échange a été accepté !")

        previous_card1 = CardsUser.objects.get(user=exchange.user1, card=exchange.card1)
        previous_card1.quantity -= 1
        if previous_card1.quantity == 0:
            previous_card1.delete()
        else:
            previous_card1.save()

        card1, created = CardsUser.objects.get_or_create(user=exchange.user2, card=exchange.card1, defaults={'quantity': 1})
        if created:
            card1.save()
        else:
            card1.quantity += 1
            card1.save()

        previous_card2 = CardsUser.objects.get(user=exchange.user2, card=exchange.card2)
        previous_card2.quantity -= 1
        if previous_card2.quantity == 0:
            previous_card2.delete()
        else:
            previous_card2.save()

        card2, created = CardsUser.objects.get_or_create(user=exchange.user1, card=exchange.card2, defaults={'quantity': 1})
        if created:
            card2.save()
        else:
            card2.quantity += 1
            card2.save()
    # Annulé : on ne fait pas l'échange
    elif (exchange.user1_response == 'NOK' or exchange.user2_response == 'NOK') and exchange.status != 'Refusé':
        exchange.status = 'Refusé'
        exchange.save()
        messages.success(request, f"L'échange a été annulé")

    return redirect('exchange_status', exchange_id=exchange.id)


# Echange : user1 ou 2 a annulé l'échange
def cancel_exchange(request, exchange_id):
    exchange = get_object_or_404(Exchange, pk=exchange_id)

    if request.user == exchange.user1:
        exchange.user1_response = "NOK"
        exchange.save()
        messages.success(request, f"Vous avez bien annulé cet échange")
    elif request.user == exchange.user2:
        exchange.user2_response = "NOK"
        exchange.save()
        messages.success(request, f"Vous avez bien annulé cet échange")
    else:
        messages.error(request, f"Vous n'êtes pas autorisé à annuler cet échange")

    exchange.status = 'Refusé'
    exchange.save()
    messages.success(request, f"L'échange a été annulé")

    return redirect('exchange_status', exchange_id=exchange.id)


# Echange : statut de l'échange
def exchange_status(request, exchange_id):
    exchange = get_object_or_404(Exchange, pk=exchange_id)
    context = {
        'exchange': exchange,
    }
    return render(request, 'hearthstone/exchange_status.html', context)


# Echange : page pour le user2 de sélectionner une carte d'échange
def exchange_choose(request, exchange_id):
    exchange = get_object_or_404(Exchange, pk=exchange_id)
    profile = get_object_or_404(Profile, pk=request.user.id)

    context = {
        'exchange': exchange,
        'profile': profile,
    }
    return render(request, 'hearthstone/exchange_choose.html', context)


# Echange : user1 ou user2 a refusé la proposition
def exchange_refuse(request, exchange_id):
    exchange = get_object_or_404(Exchange, pk=exchange_id)
    context = {
        'exchange': exchange,
    }
    return render(request, 'hearthstone/exchange_refuse.html', context)


def sell(request, card_id):
    card = get_object_or_404(Card, pk=card_id)
    card_to_sell = CardsUser.objects.get(user=request.user, card=card)
    if card_to_sell is not None:
        activity = Activity.objects.create(
            author=request.user,
            content=request.user.username + " a vendu la carte : " + card.title,
            type="vente")
        card_to_sell.quantity -= 1
        if card_to_sell.quantity == 0:
            card_to_sell.delete()
        else:
            card_to_sell.save()
        profile = get_object_or_404(Profile, pk=request.user.id)
        profile.credit += 30
        profile.save()
        messages.success(request, f"Vous avez bien vendu cette carte (30 crédits)")
    else:
        messages.error(request, f"Vous ne pouvez pas vendre une carte que vous n'avez pas !")

    return redirect('myCards')
