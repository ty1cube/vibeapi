from django.apps import AppConfig


class AuthenticationAppConfig(AppConfig):
    name = 'vibe_user'
    label = 'vibe_user'
    verbose_name = 'vibespot'

    def ready(self):
        import vibe_user.signals

# This is how we register our custom app config with Django. Django is smart
# enough to look for the `default_app_config` property of each registered app
# and use the correct app config based on that value.
default_app_config = 'vibe_user.AuthenticationAppConfig'