# Generated by Django 5.1.3 on 2024-10-20 17:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mailing", "0005_remove_mailing_datetime_to_start_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="attempt",
            name="date_first_attempt",
        ),
        migrations.AlterField(
            model_name="attempt",
            name="date_last_attempt",
            field=models.DateTimeField(
                auto_now=True, verbose_name="Дата попытки"
            ),
        ),
    ]