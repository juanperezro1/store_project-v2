# Generated by Django 2.2 on 2021-01-21 14:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store_project_app', '0015_auto_20210121_0906'),
    ]

    operations = [
        migrations.AddField(
            model_name='venta',
            name='actualizacion_usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='actualizacion_usuario', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='venta',
            name='creacion_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='creacion_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='venta',
            name='fecha_actualizacion',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='venta',
            name='fecha_creacion',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
