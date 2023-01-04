# Generated by Django 4.1.4 on 2023-01-04 12:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=50)),
                ("email", models.EmailField(max_length=100)),
                ("address", models.CharField(max_length=256)),
                ("basket_history", models.JSONField(default=dict)),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "status",
                    models.SmallIntegerField(
                        choices=[
                            (0, "Created"),
                            (1, "Paid"),
                            (2, "On way"),
                            (3, "Delivered"),
                        ],
                        default=0,
                    ),
                ),
                (
                    "initiator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
