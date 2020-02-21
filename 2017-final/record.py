""" Records so we have nicer code at hashcode """
from collections import OrderedDict

class Record(OrderedDict):
    """ Record allows mutable named tuples """
    def __init__(self, *args, **kwargs):
        super(Record, self).__init__(*args, **kwargs)
        self._initialized = True

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        if hasattr(self, '_initialized'):
            super(Record, self).__setitem__(name, value)
        else:
            super(Record, self).__setattr__(name, value)

    def __repr__(self):
        desc = "{"
        for i in super(Record, self).items():
            key, value = i
            desc += '{}: {}, '.format(key, repr(value))
        desc = desc[:-2]
        desc += "}"
        return desc
