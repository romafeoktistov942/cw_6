# Generated by Django 5.1.3 on 2024-10-19 11:13

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("mailing", "0003_alter_mailing_client_list_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="mailing",
            name="date_of_first_dispatch",
        ),
    ]
