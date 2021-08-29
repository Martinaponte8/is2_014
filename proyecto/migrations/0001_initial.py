
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rol', '0001_initial'),

    ]

    operations = [
        migrations.CreateModel(

            name='Proyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
                ('fecha_inicio', models.DateField(verbose_name='Fecha de Inicio Proyecto')),
                ('fecha_fin', models.DateField(verbose_name='Fecha de Fin Proyecto')),
                ('estado', models.CharField(choices=[('Pendiente', 'Pendiente'), ('Activo', 'Activo'), ('Cancelado', 'Cancelado'), ('Terminado', 'Terminado'), ('Suspendido', 'Suspendido')], default='PEN', max_length=25)),
                ('descripcion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ProyectoDetalle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyecto.proyecto')),
                ('rol', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rol.rol')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Flujo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
                ('descripcion', models.TextField()),
                ('proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyecto.proyecto')),
            ],
        ),
        migrations.CreateModel(
            name='Fase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
                ('estado', models.CharField(choices=[('To Do', 'To Do'), ('Doing', 'Doing'), ('Do', 'Do')], default='To Do', max_length=25)),
                ('flujo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyecto.flujo')),

            name='Fase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
                ('estado', models.CharField(choices=[('To Do', 'To Do'), ('Doing', 'Doing'), ('Do', 'Do')], default='To Do', max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Flujo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
                ('descripcion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
                ('fecha_inicio', models.DateField(verbose_name='Fecha de Inicio Proyecto')),
                ('fecha_fin', models.DateField(verbose_name='Fecha de Fin Proyecto')),
                ('estado', models.CharField(choices=[('Pendiente', 'Pendiente'), ('Activo', 'Activo'), ('Cancelado', 'Cancelado'), ('Terminado', 'Terminado'), ('Suspendido', 'Suspendido')], default='PEN', max_length=25)),
                ('descripcion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ProyectoDetalle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyecto.proyecto')),
                ('rol', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rol.rol')),

            ],
        ),
    ]
