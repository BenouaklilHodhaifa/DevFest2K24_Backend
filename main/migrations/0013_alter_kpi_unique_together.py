# Generated by Django 5.0.6 on 2024-10-25 22:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0012_alter_kpi_unique_together"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="kpi",
            unique_together=set(),
        ),
    ]