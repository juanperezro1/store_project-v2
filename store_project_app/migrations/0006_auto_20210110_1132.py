# Generated by Django 2.2 on 2021-01-10 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_project_app', '0005_auto_20210110_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='fecha_vencimiento',
            field=models.DateField(blank=True, null=True),
        ),
    ]
