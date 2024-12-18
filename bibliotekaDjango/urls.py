from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from ksiazkiWeb import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ksiazki/', include('ksiazkiWeb.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('rejestracja/', views.rejestracja, name='rejestracja'),
    path('profil/', views.profil, name='profil'),
    path('ustawienia/', views.ustawienia, name='ustawienia'),
    path('wypozycz/<int:ksiazka_id>/', views.wypozycz_ksiazke, name='wypozycz_ksiazke'),
    path('sprawdz_dostepnosc/<int:ksiazka_id>/', views.sprawdz_dostepnosc, name='sprawdz_dostepnosc'),
    path('zwroc_ksiazke/<int:wypozyczenie_id>/', views.zwroc_ksiazke, name='zwroc_ksiazke'),

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
