# Generated by Django 5.1.7 on 2025-03-27 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='is_favorite',
            field=models.BooleanField(default=False),
        ),
    ]
