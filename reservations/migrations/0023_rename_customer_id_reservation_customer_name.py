# Generated by Django 3.2.9 on 2021-12-19 09:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0022_alter_reservation_customer_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservation',
            old_name='customer_id',
            new_name='customer_name',
        ),
    ]