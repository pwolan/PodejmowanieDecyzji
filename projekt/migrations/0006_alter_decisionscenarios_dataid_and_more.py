# Generated by Django 4.2.6 on 2023-11-16 10:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("projekt", "0005_alter_decisionscenarios_dataid_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="decisionscenarios",
            name="dataID",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="projekt.data",
            ),
        ),
        migrations.AlterField(
            model_name="decisionscenarios",
            name="modelID",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="projekt.models",
            ),
        ),
        migrations.AlterField(
            model_name="decisionscenarios",
            name="weightID",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="projekt.weights",
            ),
        ),
    ]
