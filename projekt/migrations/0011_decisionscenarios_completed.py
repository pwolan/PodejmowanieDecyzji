# Generated by Django 4.2.7 on 2023-12-27 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projekt', '0010_alter_models_aggregation_method_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='decisionscenarios',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
