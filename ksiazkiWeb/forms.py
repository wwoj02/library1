from django.forms import ModelForm
from .models import Ksiazka, Wypozyczenie
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class KsiazkaForm(ModelForm):
    class Meta:
        model = Ksiazka
        fields = ['tytul','autor','rok','opis','premiera','ocena','obraz']


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class WypozyczenieForm(forms.ModelForm):
    class Meta:
        model = Wypozyczenie
        fields = ['ksiazka', 'termin_zwrotu']
        widgets = {
            'termin_zwrotu': forms.DateInput(attrs={'type': 'date'}),
        }