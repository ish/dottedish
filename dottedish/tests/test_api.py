import unittest
from dottedish import api


class TestAPI(unittest.TestCase):

    def test_wrapping(self):
        s = ''
        self.assertTrue(s is api.wrap(s))
        self.assertTrue(s is api.unwrap(s))

    def test_setitem_no_impl(self):
        self.assertRaises(NotImplementedError, api.set, '', 'foo', 0)

    def test_getitem_no_impl(self):
        self.assertRaises(NotImplementedError, api.get, '', 'foo')

