class AttributeDict(dict):

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            # to conform with __getattr__ spec
            raise AttributeError(key)

    def __setattr__(self, key, value):
        self[key] = value


class AttributeSet(set):

    def __repr__(self):
        return '{%s}' % ', '.join(repr(obj) for obj in self)
