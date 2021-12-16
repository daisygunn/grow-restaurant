# Generated by Django 3.2.9 on 2021-12-15 18:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reservations', '0014_auto_20211214_1242'),
    ]

    operations = [
        # migrations.AlterField(
        #     model_name='customer',
        #     name='email',
        #     field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_email', to=settings.AUTH_USER_MODEL),
        # ),
        migrations.AlterField(
            model_name='customer',
            name='full_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(
                max_length=128, null=True, region=None),
        ),
    ]
