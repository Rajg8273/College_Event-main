# Generated by Django 4.2.1 on 2024-02-28 09:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="event",
            name="organizer_upload",
        ),
    ]