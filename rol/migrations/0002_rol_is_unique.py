# Generated by Django 3.2.6 on 2021-09-15 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rol', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rol',
            name='is_unique',
            field=models.BooleanField(default=False, verbose_name='Es único en el proyecto'),
        ),
    ]
