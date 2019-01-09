from django.contrib import admin
from .models import Card, Deck, Battle

# Register your models here.
admin.site.register(Card)
admin.site.register(Deck)
admin.site.register(Battle)
