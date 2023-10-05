# Generated by Django 4.2.5 on 2023-10-04 21:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Bills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('bill_name', models.CharField(max_length=200)),
                ('bill_due_date', models.DateField()),
                ('bill_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='billsManager.subcategory')),
            ],
        ),
    ]