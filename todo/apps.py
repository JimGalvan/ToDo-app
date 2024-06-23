from django.apps import AppConfig


class ThemeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'theme'


class SignalsConfig(AppConfig):
    name = 'todo'

    def ready(self):
        from .signals import create_default_todo_lists, ensure_main_list_on_delete, ensure_main_list_on_save
