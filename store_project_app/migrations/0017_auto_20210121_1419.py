# Generated by Django 2.2 on 2021-01-21 19:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store_project_app', '0016_auto_20210121_0926'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venta',
            name='actualizacion_usuario',
        ),
        migrations.RemoveField(
            model_name='venta',
            name='creacion_user',
        ),
        migrations.RemoveField(
            model_name='venta',
            name='fecha_actualizacion',
        ),
        migrations.RemoveField(
            model_name='venta',
            name='fecha_creacion',
        ),
    ]