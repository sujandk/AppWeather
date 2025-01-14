# Generated by Django 5.1.4 on 2025-01-13 21:47

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="city",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="time",
            name="date",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="base.date"
            ),
        ),
    ]