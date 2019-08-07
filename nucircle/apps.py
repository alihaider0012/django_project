from django.apps import AppConfig
from django.db.models.signals import post_save


class NucircleConfig(AppConfig):
    name = 'nucircle'
    def ready(self):
        import nucircle.signals