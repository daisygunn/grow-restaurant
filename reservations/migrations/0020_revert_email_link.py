# Generated by Django 3.2.9 on 2021-12-16 20:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0019_customer_email_link'),
    ]

    operations = [
        migrations.RemoveField(
        model_name='customer',
        name='email',
    ),
        migrations.RenameField(
        model_name='customer',
        old_name='email_link',
        new_name='email',
    ),
]