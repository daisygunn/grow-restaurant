# Generated by Django 3.2.9 on 2021-12-10 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0003_reservations_table_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tables',
            name='min_no_people',
        ),
        migrations.AlterField(
            model_name='reservations',
            name='no_of_guests',
            field=models.IntegerField(choices=[(1, '1 person'), (2, '2 people'), (3, '3 people'), (4, '4 people')], default=1),
        ),
    ]