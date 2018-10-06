from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.

def home(request):
    title = 'Accueil'
    test = 'wow'
    context = {
        'title': title,
        'test': test,
    }
    return render(request, 'hearthstone/index.html', context)

def register(request):
    return render(request, 'registration/register.html')

def game(request):
    return render(request, 'hearthstone/game.html')

def test(request):
    test = 'hehe'
    return render(request, 'hearthstone/test.html', {'test': test})
