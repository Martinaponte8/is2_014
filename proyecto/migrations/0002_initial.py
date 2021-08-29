# Generated by Django 3.2.6 on 2021-08-29 03:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('proyecto', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='proyectodetalle',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='flujo',
            name='proyecto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyecto.proyecto'),
        ),
        migrations.AddField(
            model_name='fase',
            name='flujo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyecto.flujo'),
        ),
    ]