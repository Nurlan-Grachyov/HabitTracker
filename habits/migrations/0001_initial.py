# Generated by Django 5.2 on 2025-04-11 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Habits",
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
                (
                    "place",
                    models.CharField(max_length=30, verbose_name="место привычки"),
                ),
                (
                    "start_time",
                    models.TimeField(verbose_name="время начала выполнения привычки"),
                ),
                ("action", models.CharField(verbose_name="действие привычки")),
                (
                    "sign_pleasant_habit",
                    models.CharField(
                        max_length=50, verbose_name="признак приятной привычки"
                    ),
                ),
                (
                    "related_habit",
                    models.CharField(max_length=50, verbose_name="связанная привычка"),
                ),
                (
                    "periodicity",
                    models.PositiveSmallIntegerField(
                        default=1, verbose_name="Периодичность"
                    ),
                ),
                (
                    "reward",
                    models.CharField(max_length=50, verbose_name="вознаграждение"),
                ),
                (
                    "time_to_complete",
                    models.TimeField(verbose_name="время для выполнения привычки"),
                ),
                ("is_public", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name": "привычка",
                "verbose_name_plural": "привычки",
            },
        ),
    ]
