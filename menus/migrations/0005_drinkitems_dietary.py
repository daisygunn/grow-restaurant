# Generated by Django 3.2.9 on 2022-01-07 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0004_alter_drinkitems_allergens'),
    ]

    operations = [
        migrations.AddField(
            model_name='drinkitems',
            name='dietary',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
