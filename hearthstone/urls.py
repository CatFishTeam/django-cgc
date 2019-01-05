from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('game', views.game, name='game'),
    path('launchGame/<int:deck_id>', views.launchGame, name='launchGame'),

    path('card/<int:card_id>', views.card, name='card'),
    path('buy-cards', views.buyCards, name='buyCards'),
    path('my-cards', views.myCards, name='myCards'),
    path('my-decks', views.myDecks, name='myDecks'),
    path('create-deck', views.createDeck, name='createDeck'),
    path('save-deck', views.saveDeck, name='saveDeck'),
    path('show-deck/<int:deck_id>', views.showDeck, name='showDeck'),
    path('delete-deck/<int:deck>', views.deleteDeck, name='deleteDeck'),


    path('register', views.register, name='register'),
    path('login', auth_views.LoginView.as_view(template_name='registration/login.html'), name='app_login'),
    path('logout', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='app_logout'),

    path('profile', views.profile, name='profile'),
    path('change-password', views.changePassword, name='changePassword'),


    path('forum', views.forum, name='forum'),
    path('create-topic', views.createTopic, name='createTopic'),
    path('topic/<int:topic_id>', views.topic, name='topic'),
    path('profile', views.profile, name='profile'),
    path('change-password', views.changePassword, name='changePassword'),
    path('community', views.community, name='community'),
]
