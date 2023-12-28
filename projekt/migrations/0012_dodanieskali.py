from django.db import migrations, models

def add_initial_data(apps, schema_editor):
    Scales = apps.get_model("projekt", "Scales")
    if not Scales.objects.filter(value=0.25).exists():
        Scales.objects.create(value=0.25, description="4 razy gorsze")
        Scales.objects.create(value=1/3, description="3 razy gorsze")
        Scales.objects.create(value=0.5, description="2 razy gorsze")
        Scales.objects.create(value=1, description="Porównywalne")
        Scales.objects.create(value=2, description="2 razy lepsze")
        Scales.objects.create(value=3, description="3 razy lepsze")
        Scales.objects.create(value=4, description="4 razy lepsze")

class Migration(migrations.Migration):

    dependencies = [
        ('projekt', '0011_decisionscenarios_completed'),  # Zależność od poprzedniej migracji
    ]

    operations = [
        migrations.RunPython(add_initial_data),
    ]