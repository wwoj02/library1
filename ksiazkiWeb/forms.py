from django.forms import ModelForm
from .models import Ksiazka

class KsiazkaForm(ModelForm):
    class Meta:
        model = Ksiazka
        fields = ['tytul','autor','rok','opis','premiera','ocena','obraz']
