# Generated by Django 5.1.4 on 2025-01-13 21:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0002_city_created_at_alter_time_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="city",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
