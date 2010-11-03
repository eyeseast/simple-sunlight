"""
A really simple wrapper for Sunlight's Congress API
"""
__author__ = "Chris Amico (eyeseast@gmail.com)"
__version__ = "0.1.2"
__copyright__ = "Copyright (c) 2010 Chris Amico"
__license__ = "MIT"

import os
import urllib, urllib2
try:
    import json
except ImportError:
    import simplejson as json

__all__ = ['SunlightError', 'Sunlight']

BASE_URL = "http://services.sunlightlabs.com/api/%s.json?%s"

RESPONSE_KEYS = {
    # simple keys to skip the level we already know

    'legislators.get':                  'legislator',
    'legislators.getList':              'legislators',
    'legislators.search':               'results',
    'legislators.allForZip':            'legislators',
    'legislators.allForLatLong':        'legislators',

    'districts.getDistrictsFromZip':    'districts',
    'districts.getZipsFromDistrict':    'zips',
    'districts.getDistrictFromLatLong': 'districts',
    
    'committees.getList':               'committees',
    'committees.get':                   'committee',
    'committees.allForLegislator':      'committees',
}

class SunlightError(Exception):
    "Exception for Sunlight API"


class Sunlight(object):
    """
    A really simple Sunlight API client that just returns JSON
    
    Instantiate a Sunlight object with your API key:
    
    >>> sunlight = Sunlight(API_KEY)
    >>> pelosi = sunlight.legislators.get(lastname='pelosi')
    >>> print pelosi['firstname']
    Nancy
    """
    def __init__(self, apikey=None, method=None):
        self.apikey = apikey or os.environ.get('SUNLIGHT_API_KEY', '')
        self.method = method
    
    def __getattr__(self, method):
        if self.method:
            return Sunlight(self.apikey, "%s.%s" % (self.method, method))
        else:
            return Sunlight(self.apikey, method)
    
    def __call__(self, **params):
        params['apikey'] = self.apikey
        url = BASE_URL % (self.method, urllib.urlencode(params))
        try:
            response = urllib2.urlopen(url).read()
        except Exception, e:
            raise SunlightError(e)
        
        return json.loads(response)['response'][RESPONSE_KEYS[self.method]]
    
    def __repr__(self):
        return "<Sunlight: %s>" % self.method
