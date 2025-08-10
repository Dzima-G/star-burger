from django.apps import AppConfig


class PlacesConfig(AppConfig):
    name = 'places'
    verbose_name = 'Места'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        from . import signals
