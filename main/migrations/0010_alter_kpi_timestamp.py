# Generated by Django 5.0.6 on 2024-10-25 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0009_alter_kpi_unique_together"),
    ]

    operations = [
        migrations.AlterField(
            model_name="kpi",
            name="timestamp",
            field=models.DateTimeField(),
        ),
    ]
