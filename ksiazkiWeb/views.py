from django.shortcuts import render, get_object_or_404, redirect
from .models import Ksiazka
from .forms import KsiazkaForm
from django.contrib.auth.decorators import login_required

def wszystkie_ksiazki(request):
    wszystkie = Ksiazka.objects.all() #all get filter
    # wszystkie = []
    return render(request, 'ksiazki.html', {'ksiazki': wszystkie})


@login_required()
def nowa_ksiazka(request):
    # jesli POST to accept, pliki przesylane osobno
    form = KsiazkaForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect(wszystkie_ksiazki)

    return render(request, 'nowa_ksiazka.html', {'form':form})

@login_required()
def edytuj_ksiazke(request, id):
    ksiazka = get_object_or_404(Ksiazka, pk=id)
    form = KsiazkaForm(request.POST or None, request.FILES or None, instance=ksiazka)

    if form.is_valid():
        form.save()
        return redirect(wszystkie_ksiazki)

    return render(request, 'edycja_ksiazka.html', {'form':form})

@login_required()
def usun_ksiazke(request, id):
    ksiazka = get_object_or_404(Ksiazka, pk=id)

    if request.method == "POST":
        ksiazka.delete()
        return redirect(wszystkie_ksiazki)

    return render(request, 'potwierdz.html', {'ksiazka':ksiazka})

def kategoria(request):
    # Przykładowe dane dla strony głównej
    najnowsze_ksiazki = Ksiazka.objects.all().order_by('-id')[:5]  # Ostatnie 5 książek
    liczba_ksiazek = Ksiazka.objects.count()  # Liczba wszystkich książek
    kontekst = {
        'najnowsze_ksiazki': najnowsze_ksiazki,
        'liczba_ksiazek': liczba_ksiazek,
    }
    return render(request, 'kategoria.html', kontekst)
