from django.apps import AppConfig

class MiniNotionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mini_notion'

    def ready(self):
        import mini_notion.signals