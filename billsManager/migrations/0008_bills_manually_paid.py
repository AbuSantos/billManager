# Generated by Django 4.2.5 on 2023-10-10 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billsManager', '0007_bills_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='bills',
            name='manually_paid',
            field=models.BooleanField(default=False),
        ),
    ]
