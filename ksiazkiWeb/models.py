from django.db import models

class Ksiazka(models.Model):
    tytul = models.CharField(max_length=64, blank=False, unique=True)
    autor = models.CharField(max_length=64, blank=True)
    rok = models.PositiveSmallIntegerField(default=9999)
    opis = models.TextField(default="", blank=True)
    premiera = models.DateField(null=True, blank=True)
    ocena = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    obraz = models.ImageField(upload_to="obrazy", null=True, blank=True)

    def __str__(self):
        return self.tytul_z_rokiem()

    def tytul_z_rokiem(self):
        return "{} ({})".format(self.tytul, self.rok)
