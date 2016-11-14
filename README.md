A utility meant to mimic the functionality of the ADS reference string resolver.  See https://github.com/adsabs/ADSutils for more information.

To set up, run `python setup.py develop` in a fresh Python 3.5 venv.  It will likely work in Python 3.3 & 3.4, though it has not been tested in those environments.

This will provide the CLI `ads-resolver` that will run a simple flask app capable of handling requests.  Unfortunately, it must be run from within the ads-resolver directory to work properly.

Unit tests are provided, and can be run via `nosetests`.  There is also a convenience test method to evaluate its performance on some sample request strings.

There are many TODOs that have yet to be todone.  I have tried to note the most egregious holes.
