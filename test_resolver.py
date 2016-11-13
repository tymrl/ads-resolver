import json
from nose.tools import eq_
from unittest import TestCase

from resolver import Resolver

class ResolverTestCase(TestCase):
    def setUp(self):
        self.resolver = Resolver()
        with open('refsample.json') as f:
            self.refmap = json.loads(f.read())

    def test_get_year(self):
        eq_(self.resolver.get_year('Something that someone wrote in 1989, page #'),
            '1989')
        eq_(self.resolver.get_year('Lots 234 of 20, numbers, 2003, 12983'),
            '2003')
        eq_(self.resolver.get_year('1999 is before the current date, 2210 is after'),
            '1999')
        # Not ideal behavior, but still
        eq_(self.resolver.get_year('When 1978 is in doubt, take the last 2008'),
            '2008')
        eq_(self.resolver.get_year('If there is no year, we can fix it later'),
            '....')

    def test_get_author_initial(self):
        eq_(self.resolver.get_author_initial('Very standard string'), 'V')
        eq_(self.resolver.get_author_initial('addresses lower case'), 'A')
        eq_(self.resolver.get_author_initial('(What about parens?)'), 'W')
        eq_(self.resolver.get_author_initial('D. N. Balk on initials'), 'B')

    def test_get_publication(self):
        eq_(self.resolver.get_publication('Rees , M. J. 1990, Science, 247, 817'),
            '....Sci......')
        # Make sure ApJ is handled correctly
        eq_(self.resolver.get_publication('Ok this is ApJ 2923'),
            '....ApJ......')
        eq_(self.resolver.get_publication('How about Ann Phys (Paris) overlaps?'),
            '....AnPh.....')

    def test_get_volume_and_page(self):
        eq_(self.resolver.get_volume_and_page('Vol 1234 page 2345'),
            ('1234', '2345'))
        eq_(self.resolver.get_volume_and_page('This 234 is the first page 1'),
            ('.234', '...1'))
        eq_(self.resolver.get_volume_and_page('What 989 about periods 23.'),
            ('.989', '..23'))
