# Generated by Django 2.2 on 2021-01-17 20:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store_project_app', '0012_auto_20210117_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venta',
            name='id_empleado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store_project_app.Empleado'),
        ),
    ]
