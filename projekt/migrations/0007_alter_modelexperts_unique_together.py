# Generated by Django 4.2.7 on 2023-12-12 11:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projekt', '0006_alter_experts_user'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='modelexperts',
            unique_together={('modelID', 'expertID')},
        ),
    ]
