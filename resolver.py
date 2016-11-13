import datetime
import json
import os
import re


class Resolver:
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
        current_match = None
        matches = re.findall(self.YEAR_RE, refstring)
        while matches:
            current_match = matches.pop()
            if int(current_match) < self.CURRENT_YEAR:
                return current_match
        return '....'

    def get_author_initial(self, refstring):
        match = re.search(self.AUTHOR_INITIAL_RE, refstring)
        initial = refstring[match.start()].upper() if match else None
        return initial

    def get_publication(self, refstring):
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
    def _left_pad(num_string):
        # TODO: handle page numbers greater than 4 characters correctly
        while len(num_string) < 4:
            num_string = '.' + num_string
        return num_string

    def get_volume_and_page(self, refstring):
        matches = re.findall(self.PAGE_NUM_RE, refstring)
        if not matches:
            return ('....', '....')
        # Assume that the last number is the page
        page = self._left_pad(matches.pop())
        
        # Maybe there's only one number
        if not matches:
            return ('....', page)
        
        # Assume that the next-to-last number is the volume
        volume = self._left_pad(matches.pop())
        return volume, page
