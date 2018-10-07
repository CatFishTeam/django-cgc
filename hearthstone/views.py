from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .forms import UserRegisterForm
from django.contrib import messages

from .models import Card, Deck, Game


def home(request):
    title = 'Accueil'
    context = {
        'title': title,
        'games': Game.objects.all()
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


def test(request):
    test = 'hehe'
    return render(request, 'hearthstone/test.html', {'test': test})
