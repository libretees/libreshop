import logging
from functools import wraps

logger = logging.getLogger(__name__)

UUID = 'b37d96da-006e-4ba1-945c-ca4f3b318eea'

def session_based(cls):

    methods = ['__setitem__', '__delitem__', '__iadd__', '__imul__', 'pop',
        'append', 'extend', 'insert', 'remove', 'clear', 'sort', 'reverse',
    ]

    def wrap_method(method):
        def wrapper(self, *args, **kwargs):
            value = method(self, *args, **kwargs)
            self._update_session()
            return value
        return wrapper

    for method_name in methods:
        method = wrap_method(getattr(cls, method_name))
        setattr(cls, method_name, method)

    return cls


@session_based
class SessionList(list):
    def __init__(self, session, *args, **kwargs):
        super(SessionList, self).__init__(*args, **kwargs)

        self.session = session

        if not session.has_key(UUID):
            self._update_session()
        else:
            self += session.get(UUID)


    def _update_session(self):
        self.session[UUID] = list(self)
