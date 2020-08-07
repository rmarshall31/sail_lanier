# Generated by Django 3.1 on 2020-08-07 18:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phrf', '0002_auto_20190627_2303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boat',
            name='year',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2020)]),
        ),
    ]
