from dottedish import api

@api.setitem.when_type(dict)
def setitem_dict(o, key, value):
    o[key] = value

@api.getitem.when_type(dict)
def getitem_dict(o, key, default):
    return o.get(key, default)

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


@api.unwrap.when_type(DottedDict)
def unwrap_dict(o):
    return o._o

