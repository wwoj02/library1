from django.db import models
from django.contrib.auth.models import User


class Ksiazka(models.Model):
    tytul = models.CharField(max_length=64, blank=False, unique=True)
    autor = models.CharField(max_length=64, blank=True)
    rok = models.PositiveSmallIntegerField(default=9999)
    opis = models.TextField(default="", blank=True)
    premiera = models.DateField(null=True, blank=True)
    ocena = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    obraz = models.ImageField(upload_to="obrazy", null=True, blank=True)
    dostepna = models.BooleanField(default=True)

    def __str__(self):
        return self.tytul_z_rokiem()

    def tytul_z_rokiem(self):
        return "{} ({})".format(self.tytul, self.rok)

class Wypozyczenie(models.Model):
    ksiazka = models.ForeignKey(Ksiazka, on_delete=models.CASCADE, related_name="wypozyczenia")
    uzytkownik = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wypozyczenia")
    data_wypozyczenia = models.DateField(auto_now_add=True)
    termin_zwrotu = models.DateField()
    data_zwrotu = models.DateField(null=True, blank=True)
    kara = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.uzytkownik.username} wypożyczył '{self.ksiazka.tytul}'"


