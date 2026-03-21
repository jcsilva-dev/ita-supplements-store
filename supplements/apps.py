from django.apps import AppConfig


class SupplementsConfig(AppConfig):
    name = 'supplements'


    def ready(self):
        import supplements.signails
