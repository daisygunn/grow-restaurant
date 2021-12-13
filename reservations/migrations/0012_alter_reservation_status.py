# Generated by Django 3.2.9 on 2021-12-13 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0011_remove_reservation_customer_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('confirmed', 'confirmed')], default='pending', max_length=10),
        ),
    ]
