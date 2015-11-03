import logging

logger = logging.getLogger(__name__)

UUID = 'b37d96da-006e-4ba1-945c-ca4f3b318eea'

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


    def __setitem__(self, key, value):
        super(SessionList, self).__setitem__(key, value)
        self._update_session()


    def __delitem__(self, key):
        super(SessionList, self).__delitem__(key)
        self._update_session()


    def __iadd__(self, L):
        super(SessionList, self).__iadd__(L)
        self._update_session()


    def __imul__(self, i):
        super(SessionList, self).__imul__(i)
        self._update_session()


    def append(self, x):
        super(SessionList, self).append(x)
        self._update_session()


    def extend(self, L):
        super(SessionList, self).extend(L)
        self._update_session()


    def insert(self, i, x):
        super(SessionList, self).insert(i, x)
        self._update_session()


    def remove(self, x):
        super(SessionList, self).remove(x)
        self._update_session()


    def pop(self, i):
        i = super(SessionList, self).pop(i)
        self._update_session()
        return i


    def clear(self):
        super(SessionList, self).clear()
        self._update_session()


    def sort(self):
        super(SessionList, self).sort()
        self._update_session()


    def reverse(self):
        super(SessionList, self).reverse()
        self._update_session()
