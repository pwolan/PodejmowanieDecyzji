# Generated by Django 4.2.7 on 2023-11-19 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projekt', '0007_decisionscenarios_userid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='criterias',
            name='parent_criterion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='projekt.criterias'),
        ),
    ]