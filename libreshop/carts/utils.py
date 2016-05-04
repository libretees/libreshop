import logging
from decimal import Decimal
from functools import wraps
from products.models import Variant

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
        self.session.save()


class SessionCart(list):

    def __init__(self, session, *args, **kwargs):

        self._session_list = SessionList(session, *args, **kwargs)
        # Map the PKs in the SessionList to their respective Variants and
        # populate the SessionCart.
        self += [
            variant for pk in self._session_list
            for variant in Variant.objects.filter(pk=pk) if variant.salable
        ]

        # Remove Variant PKs from the SessionList if the Variant is no longer
        # salable or if it has been deleted from the database.
        stale_items = [
            pk for pk in self._session_list
            if pk not in [item.pk for item in self]
        ]
        for pk in stale_items:
            self._session_list.remove(pk)


    @property
    def total(self):
        return (
            sum(item.price for item in self).quantize(Decimal(10) ** -2)
            if self else Decimal(0.00)
        )


    def add(self, item):
        self._session_list.append(item.pk)
        super(SessionCart, self).append(item)


    def remove(self, item):
        self._session_list.remove(item.pk)
        super(SessionCart, self).remove(item)


    def empty(self):
        del self._session_list.session[UUID]
        super(SessionCart, self).clear()
