from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Parties
    path('game', views.game, name='game'),
    path('battle/<int:battle_id>', views.battle, name='battle'),
    path('launchGame/<int:deck_id>', views.launch_game, name='launchGame'),

    # Cartes et decks
    path('open_first_deck', views.open_first_deck, name='open_first_deck'),
    path('card/<int:card_id>', views.card, name='card'),
    path('buy-cards', views.buy_cards, name='buyCards'),
    path('my-cards', views.my_cards, name='myCards'),
    path('my-decks', views.my_decks, name='myDecks'),
    path('create-deck', views.create_deck, name='createDeck'),
    path('save-deck', views.save_deck, name='saveDeck'),
    path('show-deck/<int:deck_id>', views.show_deck, name='showDeck'),
    path('delete-deck/<int:deck>', views.delete_deck, name='deleteDeck'),

    # Authentification
    path('register', views.register, name='register'),
    path('login', auth_views.LoginView.as_view(template_name='registration/login.html'), name='app_login'),
    path('logout', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='app_logout'),

    # Utilisateur
    path('profile', views.profile, name='profile'),
    path('change-password', views.change_password, name='changePassword'),
    path('user/<int:user_id>', views.user, name='user'),

    # Communauté
    path('forum', views.forum, name='forum'),
    path('create-topic', views.create_topic, name='createTopic'),
    path('topic/<int:topic_id>', views.topic, name='topic'),
    path('profile', views.profile, name='profile'),
    path('change-password', views.change_password, name='changePassword'),
    path('community', views.community, name='community'),
    path('activities', views.activities, name='activities'),
    path('subscribe/<int:user_id>', views.subscribe, name='subscribe'),
    path('exchange/<int:card_id>', views.exchange, name='exchange'),
    path('exchange_status/<int:exchange_id>', views.exchange_status, name='exchange_status'),
    path('exchange_choose/<int:exchange_id>', views.exchange_choose, name='exchange_choose'),
    path('exchange_refuse/<int:exchange_id>', views.exchange_refuse, name='exchange_refuse'),
    path('start_exchange', views.start_exchange, name='start_exchange'),
    path('continue_exchange', views.continue_exchange, name='continue_exchange'),
    path('validate_exchange/<int:exchange_id>', views.validate_exchange, name='validate_exchange'),
    path('cancel_exchange/<int:exchange_id>', views.cancel_exchange, name='cancel_exchange'),
    path('sell/<int:card_id>', views.sell, name='sell'),
    path('ladder', views.ladder, name='ladder'),
]
