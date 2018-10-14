from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .forms import UserRegisterForm
from django.contrib import messages

from .models import Card, Deck, Game


def home(request):
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


def test(request):
    test = 'hehe'
    return render(request, 'hearthstone/test.html', {'test': test})
