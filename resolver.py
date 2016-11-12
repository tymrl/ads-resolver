import datetime
import re

CURRENT_YEAR = datetime.datetime.now().year
YEAR_RE = r'19\d\d|20\d\d'

def get_year(refstring):
    current_match = None
    matches = re.findall(YEAR_RE, refstring)
    while matches:
        current_match = matches.pop()
        if int(current_match) < CURRENT_YEAR:
            return current_match
