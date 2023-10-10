# Generated by Django 4.2.5 on 2023-10-09 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billsManager', '0003_bankaccount'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='virtual_account_number',
            field=models.CharField(blank=True, max_length=16, null=True, unique=True),
        ),
        migrations.DeleteModel(
            name='BankAccount',
        ),
    ]