# Generated by Django 3.2.9 on 2021-12-19 08:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0021_auto_20211219_0755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='customer_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer', to='reservations.customer'),
        ),
    ]