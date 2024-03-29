# Generated by Django 2.2 on 2021-02-05 18:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store_project_app', '0018_auto_20210123_1305'),
    ]

    operations = [
        migrations.AddField(
            model_name='venta',
            name='usuario_venta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='usuario_venta', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='genero',
            field=models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino')], default=None, max_length=10, verbose_name='Genero'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='telefono',
            field=models.CharField(max_length=50, verbose_name='Telefono'),
        ),
        migrations.AlterField(
            model_name='venta',
            name='fecha_venta',
            field=models.DateField(default='2021-02-05'),
        ),
    ]
