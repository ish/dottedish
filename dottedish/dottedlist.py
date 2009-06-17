from dottedish import api

@api.setitem.when_type(list)
def setitem_list(o, key, value):
    o[int(key)] = value

@api.getitem.when_type(list)
def getitem_list(o, key):
    try:
        return o[int(key)]
    except IndexError:
        raise KeyError(key)

@api.wrap.when_type(list)
def wrap_list(o):
    return DottedList(o)

class DottedList(object):

    def __init__(self, o):
        self._o = o

    def __setitem__(self, key, value):
        return api.set(self._o, key, api.unwrap(value))

    def __getitem__(self, key):
        return api.get(self._o, key)

    def keys(self):
        return [str(i) for i in xrange(len(self._o))]

    def items(self):
        return [(str(i), api.wrap(value))
                for (i, value) in enumerate(self._o)]

@api.unwrap.when_type(DottedList)
def unwrap_list(o):
    return o._o

