import unittest
from dottedish import api, dottedlist


class TestAPI(unittest.TestCase):

    def test_set(self):
        # Test top-level
        l = [None]
        api.set(l, '0', 'foo')
        self.assertEquals(l, ['foo'])
        # Test nested.
        l = [[None]]
        api.set(l, '0.0', 'foo')
        self.assertEquals(l, [['foo']])
        # Test traversal key error.
        self.assertRaises(KeyError, api.set, [[None]], '1.0', 'foo')

    def test_get(self):
        self.assertTrue(api.get(['foo'], '0') == 'foo')
        self.assertTrue(api.get([['foo']], '0.0') == 'foo')
        self.assertRaises(KeyError, api.get, [], '0')

    def test_getdefault(self):
        self.assertTrue(api.get([], '0', 'foo') == 'foo')
        self.assertTrue(api.get([[]], '0.0', 'foo') == 'foo')
        self.assertRaises(KeyError, api.get, [[]], '1.0', 'foo')

    def test_wrap(self):
        l = []
        dl = api.dotted(l)
        self.assertTrue(isinstance(dl, dottedlist.DottedList))

    def test_wrap_dotted(self):
        l = []
        dl = api.dotted(l)
        self.assertTrue(isinstance(dl, dottedlist.DottedList))
        self.assertTrue(dl is api.dotted(dl))


class TestDottedList(unittest.TestCase):

    def test_getitem(self):
        dl = api.dotted(['foo', 'bar'])
        self.assertTrue(dl['0'] == 'foo')
        self.assertRaises(KeyError, dl.__getitem__, '2')

    def test_setitem(self):
        l = ['foo', 'bar']
        api.dotted(l)['0'] = 'wee'
        self.assertTrue(l[0] == 'wee')

    def test_setitem_unwrap(self):
        l = ['foo', 'bar']
        api.dotted(l)['0'] = api.dotted([])
        self.assertTrue(l[0] == [])
        self.assertTrue(not isinstance(l[0], dottedlist.DottedList))

    def test_keys(self):
        self.assertTrue(api.dotted([]).keys() == [])
        self.assertTrue(api.dotted(['foo', 'bar']).keys() == ['0', '1'])
        self.assertTrue(api.dotted([['foo']]).keys() == ['0'])

    def test_items(self):
        self.assertTrue(api.dotted([]).items() == [])
        self.assertTrue(api.dotted(['foo', 'bar']).items() == [('0', 'foo'), ('1', 'bar')])
        self.assertTrue(isinstance(api.dotted([['foo']]).items()[0][1], dottedlist.DottedList))

