# Generated by Django 4.2.6 on 2023-10-27 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("AppGameZone", "0007_alter_inventario_cantidadproducto_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="inventario",
            name="residuo",
            field=models.FloatField(blank=True, null=True),
        ),
    ]
