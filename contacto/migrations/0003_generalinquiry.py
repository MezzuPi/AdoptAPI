# Generated by Django 5.2.1 on 2025-06-15 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacto', '0002_contactform_provincia'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneralInquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('mensaje', models.TextField()),
                ('fecha_envio', models.DateTimeField(auto_now_add=True)),
                ('leido', models.BooleanField(default=False)),
            ],
        ),
    ]
