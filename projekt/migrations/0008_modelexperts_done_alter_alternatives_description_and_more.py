# Generated by Django 4.2.7 on 2023-12-27 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projekt', '0007_alter_modelexperts_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='modelexperts',
            name='done',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='alternatives',
            name='description',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='alternatives',
            name='name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='criterias',
            name='description',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='scales',
            name='value',
            field=models.FloatField(unique=True),
        ),
    ]