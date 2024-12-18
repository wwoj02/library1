from django.shortcuts import render, get_object_or_404, redirect
from .models import Ksiazka, Wypozyczenie
from .forms import KsiazkaForm, CustomUserCreationForm, WypozyczenieForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.utils.timezone import now
from datetime import timedelta
from django.http import JsonResponse

def wszystkie_ksiazki(request):
    query = request.GET.get('q')
    if query:
        wszystkie = Ksiazka.objects.filter(tytul__icontains=query)
    else:
        wszystkie = Ksiazka.objects.all()
    return render(request, 'ksiazki.html', {'ksiazki': wszystkie, 'query': query})


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
    najnowsze_ksiazki = Ksiazka.objects.all().order_by('-id')[:5]
    liczba_ksiazek = Ksiazka.objects.count()
    kontekst = {
        'najnowsze_ksiazki': najnowsze_ksiazki,
        'liczba_ksiazek': liczba_ksiazek,
    }
    return render(request, 'kategoria.html', kontekst)

def rejestracja(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profil(request):
    aktywne_wypozyczenia = Wypozyczenie.objects.filter(
        uzytkownik=request.user, data_zwrotu__isnull=True
    )

    historia_wypozyczen = Wypozyczenie.objects.filter(
        uzytkownik=request.user, data_zwrotu__isnull=False
    ).order_by('-data_zwrotu')

    context = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
        'date_joined': request.user.date_joined,
        'liczba_wypozyczen': aktywne_wypozyczenia.count(),
        'aktywne_wypozyczenia': aktywne_wypozyczenia,
        'historia_wypozyczen': historia_wypozyczen,
    }
    return render(request, 'profil.html', context)

@login_required
def ustawienia(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Twoje hasło zostało zmienione pomyślnie!')
            return redirect('ustawienia')
        else:
            messages.error(request, 'Wystąpił błąd. Proszę poprawić formularz.')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'ustawienia.html', {'form': form})

@login_required()
def wypozycz_ksiazke(request, ksiazka_id):
    ksiazka = get_object_or_404(Ksiazka, id=ksiazka_id)

    if not ksiazka.dostepna:
        messages.error(request, "Ta książka jest już wypożyczona.")
        return redirect('wszystkie_ksiazki')

    Wypozyczenie.objects.create(
        uzytkownik=request.user,
        ksiazka=ksiazka,
        termin_zwrotu=now().date() + timedelta(days=14),
    )

    ksiazka.dostepna = False
    ksiazka.save()

    messages.success(request, f"Wypożyczyłeś książkę: {ksiazka.tytul}")
    return redirect('wszystkie_ksiazki')

def sprawdz_dostepnosc(request, ksiazka_id):
    ksiazka = get_object_or_404(Ksiazka, id=ksiazka_id)
    if ksiazka.dostepna:
        return JsonResponse({"status": "success", "message": "Książka jest dostępna"})
    else:
        return JsonResponse({"status": "error", "message": "Książka jest niedostępna"})

@login_required
def zwroc_ksiazke(request, wypozyczenie_id):
    wypozyczenie = get_object_or_404(Wypozyczenie, id=wypozyczenie_id, uzytkownik=request.user)

    if wypozyczenie.data_zwrotu is not None:
        messages.error(request, "Ta książka została już wcześniej zwrócona.")
        return redirect('profil')

    wypozyczenie.data_zwrotu = now().date()
    wypozyczenie.ksiazka.dostepna = True
    wypozyczenie.ksiazka.save()
    wypozyczenie.save()

    messages.success(request, f"Książka '{wypozyczenie.ksiazka.tytul}' została pomyślnie zwrócona.")
    return redirect('profil')