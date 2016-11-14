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
        eq_(self.resolver.get_volume_and_page('No numbers'),
            ('....', '....'))
        eq_(self.resolver.get_volume_and_page('Just 1 number'),
            ('....', '...1'))

    def test_make_bibcode(self):
        eq_(self.resolver.make_bibcode('Dieters, S. W., Belloni, T., Kuulkers, E., et al. 2000, ApJ, 538, 307'),
            '2000ApJ...538..307D')
        eq_(self.resolver.make_bibcode('Onsager L 1944 Phys. Rev. 65 117'),
            '1944PhRv...65..117O')
        eq_(self.resolver.make_bibcode(None), None)
        eq_(self.resolver.make_bibcode('nineteen characters'), 'nineteen characters')

    def evaluate_refsample(self):
        """
        A convenience method to look at failed test cases. Rename to 
        test_refsample() to use.
        """
        for refstring, bibcode in self.refmap.items():
            if self.resolver.make_bibcode(refstring) != bibcode:
                print(refstring)
                print(self.resolver.make_bibcode(refstring))
                print(bibcode)
                print()
