# Generated by Django 4.2.16 on 2024-12-18 02:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ksiazkiWeb', '0004_alter_ksiazka_opis'),
    ]

    operations = [
        migrations.AddField(
            model_name='ksiazka',
            name='dostepna',
            field=models.BooleanField(default=True),
        ),
        migrations.CreateModel(
            name='Wypozyczenie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_wypozyczenia', models.DateField(auto_now_add=True)),
                ('termin_zwrotu', models.DateField()),
                ('data_zwrotu', models.DateField(blank=True, null=True)),
                ('kara', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('ksiazka', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wypozyczenia', to='ksiazkiWeb.ksiazka')),
                ('uzytkownik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wypozyczenia', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
