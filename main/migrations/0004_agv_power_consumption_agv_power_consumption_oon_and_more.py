# Generated by Django 5.0.6 on 2024-10-19 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_notification_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='agv',
            name='power_consumption',
            field=models.FloatField(default=12, help_text='Power consumption in kWh'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='agv',
            name='power_consumption_OON',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='agv',
            name='production_rate',
            field=models.FloatField(default=25, help_text='Production rate of the machine'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='agv',
            name='production_rate_OON',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cncmilling',
            name='production_rate',
            field=models.FloatField(default=23, help_text='Production rate of the machine'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cncmilling',
            name='production_rate_OON',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='leaktest',
            name='power_consumption',
            field=models.FloatField(default=12, help_text='Power consumption in kWh'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='leaktest',
            name='power_consumption_OON',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='leaktest',
            name='production_rate',
            field=models.FloatField(default=36, help_text='Production rate of the machine'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='leaktest',
            name='production_rate_OON',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='paintingrobot',
            name='power_consumption',
            field=models.FloatField(default=25, help_text='Power consumption in kWh'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='paintingrobot',
            name='power_consumption_OON',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='paintingrobot',
            name='production_rate',
            field=models.FloatField(default=20, help_text='Production rate of the machine'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='paintingrobot',
            name='production_rate_OON',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stampingpress',
            name='production_rate',
            field=models.FloatField(default=80, help_text='Production rate of the machine'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stampingpress',
            name='production_rate_OON',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='welding',
            name='production_rate',
            field=models.FloatField(default=15, help_text='Production rate of the machine'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='welding',
            name='production_rate_OON',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
