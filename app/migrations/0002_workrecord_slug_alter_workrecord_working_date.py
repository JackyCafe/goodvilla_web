# Generated by Django 4.2.11 on 2024-03-17 15:53

import datetime
from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="workrecord",
            name="slug",
            field=django_extensions.db.fields.RandomCharField(
                blank=True,
                editable=False,
                length=32,
                unique=True,
                unique_for_date="transaction_date",
            ),
        ),
        migrations.AlterField(
            model_name="workrecord",
            name="working_date",
            field=models.DateField(
                default=datetime.datetime(
                    2024, 3, 17, 15, 53, 36, 286538, tzinfo=datetime.timezone.utc
                ),
                verbose_name="工作日期",
            ),
        ),
    ]
