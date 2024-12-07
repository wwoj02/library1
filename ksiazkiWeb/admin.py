from django.contrib import admin
from .models import Ksiazka

#admin.site.register(Ksiazka)

@admin.register(Ksiazka)
class KsiazkaAdmin(admin.ModelAdmin):
    # fields, exclude
    list_display = ["tytul", "rok", "ocena"]
    list_filter = ("rok", "ocena")
    search_fields = ("tytul","opis")