# Generated by Django 4.2.1 on 2024-02-28 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0002_remove_event_organizer_upload"),
    ]

    operations = [
        migrations.AddField(
            model_name="organizer",
            name="is_organizer",
            field=models.BooleanField(default=True),
        ),
    ]
