from django.apps import AppConfig

class TwitterConfig(AppConfig):
    name = 'twitter'

    def ready(self):
        import twitter.signals  # 👈 importa las señales aquí
