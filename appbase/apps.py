from django.apps import AppConfig

from pkg_helpers.services.service_route import SESSION_ROUTE

class AppbaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appbase'
    api_prefix = f"{SESSION_ROUTE}/"
