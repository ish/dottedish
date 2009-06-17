import unittest
from dottedish import api, dotteddict


class TestAPI(unittest.TestCase):

    def test_set(self):
        # Test top-level.
        d = {}
        api.set(d, 'foo', 'bar')
        self.assertTrue(d == {'foo': 'bar'})
        # Test nested.
        d = {'foo': {}}
        api.set(d, 'foo.bar', 'rab')
        self.assertTrue(d == {'foo': {'bar': 'rab'}})
        # Test traversal key error.
        self.assertRaises(KeyError, api.set, {'foo': {}}, 'oof.bar', 'rab')

    def test_get(self):
        self.assertTrue(api.get({'foo': 'bar'}, 'foo') == 'bar')
        self.assertTrue(api.get({'foo': {'bar': 'rab'}}, 'foo.bar') == 'rab')
        self.assertRaises(KeyError, api.get, {}, 'foo')
        self.assertRaises(KeyError, api.get, {'foo': 'bar'}, 'oof.bar')

    def test_get_default(self):
        self.assertTrue(api.get({}, 'foo', 'bar') == 'bar')
        self.assertTrue(api.get({'foo': {}}, 'foo.bar', 'rab') == 'rab')
        self.assertRaises(KeyError, api.get, {'foo': 'bar'}, 'oof.bar', None)

    def test_wrap(self):
        d = {}
        dd = api.dotted(d)
        self.assertTrue(isinstance(dd, dotteddict.DottedDict))


class TestDottedDict(unittest.TestCase):

    def test_getitem(self):
        d = {'foo': 'bar'}
        dd = api.dotted(d)
        self.assertTrue(dd['foo'] == 'bar')

    def test_getitem_missing(self):
        self.assertRaises(KeyError, api.dotted({}).__getitem__, 'foo')

    def test_setitem(self):
        d = {}
        api.dotted(d)['foo'] = 'bar'
        self.assertTrue(d['foo'] == 'bar')

    def test_setitem_unwrap(self):
        d = {}
        api.dotted(d)['foo'] = api.dotted({})
        self.assertTrue(d['foo'] == {})
        self.assertTrue(not isinstance(d['foo'], dotteddict.DottedDict))

    def test_keys(self):
        self.assertTrue(api.dotted({}).keys() == [])
        self.assertTrue(api.dotted({'foo': 0, 'bar': 1}).keys() == ['foo', 'bar'])
        self.assertTrue(api.dotted({'foo': {'bar': 1}}).keys() == ['foo'])

    def test_items(self):
        self.assertTrue(api.dotted({}).keys() == [])
        self.assertTrue(api.dotted({'foo': 0, 'bar': 1}).items() == [('foo', 0), ('bar', 1)])
        self.assertTrue(isinstance(api.dotted({'foo': {'bar': 1}}).items()[0][1], dotteddict.DottedDict))

