# Generated by Django 4.1.4 on 2024-06-10 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bitcoin_emissions', '0010_alter_averageefficiency_options_and_more'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='location',
            index=models.Index(fields=['location_name'], name='bitcoin_emi_locatio_8bf835_idx'),
        ),
    ]
