from django.apps import AppConfig



class HabitsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "habits"

    def ready(self):
        from habits.signals import create_periodic_tasks
