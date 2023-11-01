# Generated by Django 4.2.6 on 2023-10-28 08:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("AppGameZone", "0009_cierrecontable_idvalorentrada"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cierrecontable",
            name="idValorEntrada",
        ),
        migrations.AddField(
            model_name="inventario",
            name="idValorEntrada",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="AppGameZone.inventario",
            ),
        ),
    ]