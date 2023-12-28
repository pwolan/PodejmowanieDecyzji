# Generated by Django 4.2.7 on 2023-12-28 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projekt', '0012_dodanieskali'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataWeights',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.FloatField()),
                ('criteriaID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projekt.criterias')),
            ],
        ),
        migrations.CreateModel(
            name='ScenarioWeights',
            fields=[
                ('weightsID', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='projekt.decisionscenarios', to_field='weightID')),
                ('dataWeights', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projekt.dataweights')),
            ],
        ),
        migrations.RemoveField(
            model_name='dataelements',
            name='weightsID',
        ),
        migrations.RemoveField(
            model_name='matrices',
            name='columnSize',
        ),
        migrations.RemoveField(
            model_name='matrices',
            name='rowSize',
        ),
        migrations.AddField(
            model_name='matrices',
            name='size',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='WeightsData',
        ),
        migrations.AddField(
            model_name='dataelements',
            name='dataWeightsID',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='projekt.dataweights'),
            preserve_default=False,
        ),
    ]
