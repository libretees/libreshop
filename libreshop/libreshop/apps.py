import warnings
from django.apps import AppConfig
from django.utils.deprecation import RemovedInDjango110Warning


class PythonSocialAuthConfig(AppConfig):
    name = 'social.apps.django_app.default'

    def ready(self):
        '''
        Suppress `RemovedInDjango110Warning` warning messages for the
        python-social-auth app.
        '''
        warnings.simplefilter('ignore', RemovedInDjango110Warning)
