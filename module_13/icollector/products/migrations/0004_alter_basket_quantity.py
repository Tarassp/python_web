# Generated by Django 4.1.4 on 2023-01-04 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0003_basket_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="basket",
            name="quantity",
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
