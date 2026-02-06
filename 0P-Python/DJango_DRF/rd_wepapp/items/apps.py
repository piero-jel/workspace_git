from django.apps import AppConfig # type: ignore pylint: disable=import-error, disable=unused-import


class ItemsConfig(AppConfig):
    '''
    Docstring for ItemsConfig
    '''
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'items'
