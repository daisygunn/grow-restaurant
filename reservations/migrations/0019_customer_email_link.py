# Generated by Django 3.2.9 on 2021-12-16 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0018_transfer_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='email_link',
            field=models.EmailField(default='', max_length=254, unique=True),
        ),
    ]
