# Generated by Django 4.0.4 on 2022-04-27 00:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AppCoder', '0005_curso_duracion_alter_estudiante_mail'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profesor',
            options={'verbose_name': 'Profesor', 'verbose_name_plural': 'Profesores'},
        ),
    ]
