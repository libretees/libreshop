from django.test import LiveServerTestCase

class DjangoStep(LiveServerTestCase):

    def __init__(self, context, **kwargs):
        self.context = context
        self.impl(self.context, **kwargs)

    def impl(self, context, arguments=None):
        raise NotImplementedError('This class is not intended to be used directly.')

    __code__ = impl.__code__
