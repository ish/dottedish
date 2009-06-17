from dottedish import api

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

    def keys(self):
        return list(self.iterkeys())

    def iterkeys(self):
        return (str(key) for key in self._o.iterkeys())

    def items(self):
        return list(self.iteritems())

    def iteritems(self):
        return ((str(key), api.wrap(value))
                for (key, value) in self._o.iteritems())

@api.unwrap.when_type(DottedDict)
def unwrap_dict(o):
    return o._o

