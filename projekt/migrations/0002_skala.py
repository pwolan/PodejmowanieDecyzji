from django.db import migrations, models

def add_initial_data(apps, schema_editor):
    Scales = apps.get_model("projekt", "Scales")
    scales = [[0.125, "8 times worse"], [1/7, "7 times worse"], [1/6, "6 times worse"], [0.2, "5 times worse"],
              [0.25, "4 times worse"], [1/3, "3 times worse"], [0.5, "2 times worse"], [1, "comparable"],
              [2, "2 times better"], [3, "3 times better"], [4, "4 times better"], [5, "5 times better"],
              [6, "6 times better"], [7, "7 times better"], [8, "8 times better"]]
    for scale in scales:
        if not Scales.objects.filter(value=scale[0]).exists():
            Scales.objects.create(value=scale[0], description=scale[1])

class Migration(migrations.Migration):

    dependencies = [
        ('projekt', '0001_initial'),  # Zależność od poprzedniej migracji
    ]

    operations = [
        migrations.RunPython(add_initial_data),
    ]