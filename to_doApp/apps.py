from django.apps import AppConfig


class ToDoappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "to_doApp"

    def ready(self) -> None:
        import to_doApp.signals
