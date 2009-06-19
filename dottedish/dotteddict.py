from dottedish import api
from UserDict import UserDict

@api.setitem.when_type(dict)
def setitem_dict(o, key, value):
    o[key] = value

@api.getitem.when_type(dict)
def getitem_dict(o, key):
    return o[key]

@api.wrap.when_type(dict)
def wrap_dict(o):
    return DottedDict(o)

class DottedDict(object):

    def __init__(self, o):
        self._o = o

    def __setitem__(self, key, value):
        return api.set(self._o, key, api.unwrap(value))

    def __getitem__(self, key):
        return api.get(self._o, key)

    def get(self, key, default=None):
        return api.get(self._o, key, default=default)

    def __len__(self):
        return len(self._o)

    def keys(self):
        return list(self.iterkeys())

    def iterkeys(self):
        return (str(key) for key in self._o.iterkeys())

    def items(self):
        return list(self.iteritems())

    def iteritems(self):
        return ((str(key), api.wrap(value))
                for (key, value) in self._o.iteritems())

    def __eq__(self,other):
        if isinstance(other, DottedDict):
            return self._o == other._o
        return self._o == other

    def __iter__(self):
        for k in self._o:
            yield k

@api.unwrap.when_type(DottedDict)
def unwrap_dict(o):
    return o._o

