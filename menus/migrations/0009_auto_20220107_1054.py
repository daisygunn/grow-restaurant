# Generated by Django 3.2.9 on 2022-01-07 10:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0008_auto_20220107_1045'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DrinkItems',
            new_name='DrinkItem',
        ),
        migrations.RenameModel(
            old_name='FoodItems',
            new_name='FoodItem',
        ),
    ]