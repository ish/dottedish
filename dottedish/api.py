__all__ = ['dotted', 'set', 'get']


from simplegeneric import generic


##
# High-level API.

_sentinel = object()

def dotted(o):
    return wrap(o)

def set(o, key, value):
    parent, key = _parent_and_key(o, key)
    setitem(parent, key, value)

def get(o, key, default=_sentinel):
    return wrap(_get(o, key, default))


##
# Extension API.

@generic
def setitem(o, key, value):
    raise NotImplementedError()

@generic
def getitem(o, key):
    raise NotImplementedError()

@generic
def wrap(o):
    return o

@generic
def unwrap(o):
    return o


##
# Internal implemenation.

def _parent_and_key(o, key):
    key = key.split('.')
    parent_key, item_key = key[:-1], key[-1]
    if parent_key:
        o = _get(o, '.'.join(parent_key))
    return o, item_key

def _get(o, key, default=_sentinel):
    key = key.split('.')
    parent_key, item_key = key[:-1], key[-1]
    for k in parent_key:
        o = getitem(o, k)
    try:
        return getitem(o, item_key)
    except KeyError:
        if default is _sentinel:
            raise
        else:
            return default

