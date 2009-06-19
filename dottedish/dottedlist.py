from dottedish import api

@api.setitem.when_type(list)
def setitem_list(o, key, value):
    # Allow a new item to be appended to the list by setting the next item.
    # XXX I think this is a hack to allow lists to created and filled during
    # unflatten. Personally, I would much, much rather see the unflattened
    # graph treated as a nested mapping.
    if int(key) == len(o):
        o.append(value)
    else:
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

    def get(self, key, default=None):
        return api.get(self._o, key, default=default)

    def __len__(self):
        return len(self._o)

    def keys(self):
        return list(self.iterkeys())

    def iterkeys(self):
        return (str(i) for i in xrange(len(self._o)))

    def items(self):
        return list(self.iteritems())

    def iteritems(self):
        return ((str(i), api.wrap(value))
                for (i, value) in enumerate(self._o))

    def __eq__(self,other):
        if isinstance(other, DottedList):
            return self._o == other._o
        return self._o == other

    def __iter__(self):
        for v in self._o:
            yield api.wrap(v)

    def __contains__(self, key):
        return key in self._o

@api.unwrap.when_type(DottedList)
def unwrap_list(o):
    return o._o

