# Generated by Django 4.1 on 2024-05-21 13:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Stock", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="stock_info",
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
                ("stock_renew_date", models.CharField(max_length=25)),
            ],
        ),
    ]