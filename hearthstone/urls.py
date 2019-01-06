from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('game', views.game, name='game'),
    path('launchGame/<int:deck_id>', views.launch_game, name='launchGame'),

    path('card/<int:card_id>', views.card, name='card'),
    path('buy-cards', views.buy_cards, name='buyCards'),
    path('my-cards', views.my_cards, name='myCards'),
    path('my-decks', views.my_decks, name='myDecks'),
    path('create-deck', views.create_deck, name='createDeck'),
    path('save-deck', views.save_deck, name='saveDeck'),
    path('show-deck/<int:deck_id>', views.show_deck, name='showDeck'),
    path('delete-deck/<int:deck>', views.delete_deck, name='deleteDeck'),


    path('register', views.register, name='register'),
    path('login', auth_views.LoginView.as_view(template_name='registration/login.html'), name='app_login'),
    path('logout', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='app_logout'),

    path('profile', views.profile, name='profile'),
    path('change-password', views.change_password, name='changePassword'),
    path('user/<int:user_id>', views.user, name='user'),


    path('forum', views.forum, name='forum'),
    path('create-topic', views.create_topic, name='createTopic'),
    path('topic/<int:topic_id>', views.topic, name='topic'),
    path('profile', views.profile, name='profile'),
    path('change-password', views.change_password, name='changePassword'),
    path('community', views.community, name='community'),
    path('activities', views.activities, name='activities'),
]
