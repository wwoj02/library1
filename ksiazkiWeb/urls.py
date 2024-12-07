from django.urls import path
from ksiazkiWeb.views import wszystkie_ksiazki, nowa_ksiazka, edytuj_ksiazke, usun_ksiazke, kategoria

urlpatterns = [
    path('wszystkie/', wszystkie_ksiazki, name="wszystkie_ksiazki"),
    path('nowa/', nowa_ksiazka, name="nowa_ksiazka"),
    path('edycja/<int:id>', edytuj_ksiazke, name="edytuj_ksiazke"),
    path('usun/<int:id>', usun_ksiazke, name="usun_ksiazke"),
    path('kategoria/', kategoria, name="kategoria"),
]
