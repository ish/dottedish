from dottedish import api

@api.setitem.when_type(list)
def setitem_list(o, key, value):
    o[int(key)] = value

@api.getitem.when_type(list)
def getitem_list(o, key, default):
    try:
        return o[int(key)]
    except IndexError:
        return default

@api.wrap.when_type(list)
def wrap_list(o):
    return DottedList(o)

class DottedList(object):

    def __init__(self, o):
        self._o = o

    def __setitem__(self, key, value):
        return api.set(self._o, key, value)

    def __getitem__(self, key):
        return api.get(self._o, key)

