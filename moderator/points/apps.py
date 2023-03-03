from django.apps import AppConfig


class PointsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'moderator.points'

    def ready(self):
        from .signals import function_case, receivers
