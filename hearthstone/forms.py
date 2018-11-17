from django import forms
from django.contrib.auth.models import User
from .models import Topic, Message
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class TopicCreationForm(ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'content']

class MessageCreationForm(ModelForm):
    content = forms.CharField(label="Message")
    class Meta:
        model = Message
        fields = ['content']
