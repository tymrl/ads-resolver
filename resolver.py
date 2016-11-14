import datetime
import json
import os
import re


class Resolver:
    """
    A class for turning a reference string into a standard bibliographic code.
    It provides a holding place for a number of relevant regexes, as well as
    mapping from common references to publications to a standardized
    abbreviations.
    """
    def __init__(self):
        # TODO: update for long-running installations
        self.CURRENT_YEAR = datetime.datetime.now().year
        self.YEAR_RE = r'19\d\d|20\d\d'
        self.AUTHOR_INITIAL_RE = r'[a-zA-Z]{2,}?'
        self.PAGE_NUM_RE = r'\d+'
        # TODO: protect against being run from different locations        
        with open('publications.json') as f:
            self.publications = json.load(f)

    def get_year(self, refstring):
        """
        Determine the year of the publication.  It looks for anything of the
        form 19XX or 20XX, at least when 20XX is less than the current year.
        It then takes the last one, which works more often than you might
        think.
        """
        current_match = None
        matches = re.findall(self.YEAR_RE, refstring)
        while matches:
            current_match = matches.pop()
            if int(current_match) < self.CURRENT_YEAR:
                return current_match
        return '....'

    def get_author_initial(self, refstring):
        """
        Determine the author's last initial.  Generally, this is the first
        letter of the reference string, but occasionally there are first
        initials.  We take the first letter character that is followed by
        another letter.
        """
        match = re.search(self.AUTHOR_INITIAL_RE, refstring)
        initial = refstring[match.start()].upper() if match else None
        return initial

    def get_publication(self, refstring):
        """
        Get the publication abbreviation.  We do this by going through the
        ENTIRE list of publication mentions (apologies) and finding any that
        appear in our reference string.  Because some of the mentions of
        publications match, we take the longest one, as it's very possible
        for one mention to completely contain another.
        """
        matches = {}
        # TODO: Improve performance
        for publication, code in self.publications.items():
            if publication in refstring:
                matches[publication] = code

        # If we don't have matches, just return placeholders
        if not matches:
            return '.............'

        # When in doubt, take the longest match, in case there're overlaps
        match = sorted([m for m in matches], key=len)[-1]

        # Once we have the match, looking it up is cheap
        return self.publications[match]

    @staticmethod
    def _convert_volume_and_page(num_string):
        """
        A convenience method to guarantee that our string is four characters,
        left-padded with periods or truncated if necessary.  Does not handle
        num_strings with more than four characters gracefully.
        """
        while len(num_string) < 4:
            num_string = '.' + num_string
        # TODO: handle numbers with greater than 4 characters correctly
        return num_string[:4]

    def get_volume_and_page(self, refstring):
        """
        Grab the last two numbers of the refstring and assume they're the
        volume and page number, respectively.
        """
        matches = re.findall(self.PAGE_NUM_RE, refstring)
        # Assume that the last number is the page
        page = self._convert_volume_and_page(matches.pop()) if matches else '....'
        # Assume that the next-to-last number is the volume
        volume = self._convert_volume_and_page(matches.pop()) if matches else '....'
        return volume, page

    def make_bibcode(self, refstring):
        """
        Take a refstring and put together the bibcode representing it.  We do
        this by first looking up the publication, which will occasionally have
        a year attached to it.  If it does not, we look up the year, then the
        volume & page number, and finally the author's initial.
        """
        if not refstring or len(refstring) == 19:
            # If it evaluates to False, return it. If it's 19 characters long,
            # assume it's a bibcode and we want to return it.
            return refstring

        # TODO: Factor out this functionality into a Bibcode class, so we don't
        # have to deal with lists of characters as opposed to strings.
        bibcode = list('...................')
        bibcode[:13] = list(self.get_publication(refstring))
        # Check to see if we don't already have a year
        if bibcode[0] == '.':
            bibcode[:4] = list(self.get_year(refstring))

        volume, page = self.get_volume_and_page(refstring)
        bibcode[9:13] = volume
        # Note that there's a character missing here: the publication qualifier
        bibcode[14:18] = page
        bibcode[18] = self.get_author_initial(refstring)

        return ''.join(bibcode)
