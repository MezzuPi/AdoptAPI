# Generated by Django 5.2.1 on 2025-06-15 14:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animales', '0006_decision'),
    ]

    operations = [
        migrations.AddField(
            model_name='animal',
            name='fecha_creacion',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
