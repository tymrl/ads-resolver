import datetime
import re

CURRENT_YEAR = datetime.datetime.now().year
YEAR_RE = r'19\d\d|20\d\d'
AUTHOR_INITIAL_RE = r'[a-zA-Z]{2,}?'

def get_year(refstring):
    current_match = None
    matches = re.findall(YEAR_RE, refstring)
    while matches:
        current_match = matches.pop()
        if int(current_match) < CURRENT_YEAR:
            return current_match

def get_author_initial(refstring):
    match = re.search(AUTHOR_INITIAL_RE, refstring)
    initial = refstring[match.start()].upper() if match else None
    return initial
