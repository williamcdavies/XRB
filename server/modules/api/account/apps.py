from django.apps import AppConfig

class AccountConfig(AppConfig):
    name = 'modules.api.account'
    label = 'api_account'

    def ready(self):
        from modules.api.account import signals  # noqa: F401
