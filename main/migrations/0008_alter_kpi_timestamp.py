# Generated by Django 5.0.6 on 2024-10-25 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0007_kpi"),
    ]

    operations = [
        migrations.AlterField(
            model_name="kpi",
            name="timestamp",
            field=models.DateTimeField(unique=True),
        ),
    ]
