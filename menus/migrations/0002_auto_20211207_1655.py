# Generated by Django 3.2.9 on 2021-12-07 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='drinkitems',
            name='drinks_menu_section',
            field=models.IntegerField(choices=[(0, 'Hot Drinks'), (1, 'Fruit juices/Soft Drinks'), (2, 'Wine/Beer/Cocktails'), (3, 'New item')], default=3),
        ),
        migrations.AddField(
            model_name='fooditems',
            name='food_menu_section',
            field=models.IntegerField(choices=[(0, 'Breakfast/Brunch'), (1, 'Dinner'), (2, 'New item')], default=2),
        ),
    ]
