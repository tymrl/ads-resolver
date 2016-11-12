import json
from nose.tools import eq_
from unittest import TestCase

from resolver import get_year

class ResolverTestCase(TestCase):
    def setUp(self):
        with open('refsample.json') as f:
            self.refmap = json.loads(f.read())

    def test_get_year(self):
        eq_(get_year('Something that someone wrote in 1989, page'), '1989')
        eq_(get_year('Lots 234 of 20, numbers, 2003, 12983'), '2003')
        eq_(get_year('2210 is after the current date, 1999 is not'), '1999')
        # Not ideal behavior, but still.
        eq_(get_year('When 1978 is in doubt, take the last 2008'), '2008')
        eq_(get_year('If there is no year, we can fix it later'), None)
