# Generated by Django 4.1 on 2024-05-11 14:22

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="stock_data",
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
                ("stock_symbol", models.CharField(max_length=10)),
                ("date", models.CharField(max_length=25)),
                ("total_capacity", models.IntegerField()),
                (
                    "total_turnover",
                    models.DecimalField(decimal_places=2, max_digits=20),
                ),
                ("open_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("high_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("low_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("close_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("change_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("trans_action", models.IntegerField()),
            ],
        ),
    ]
