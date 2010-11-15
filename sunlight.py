"""
A really simple wrapper for Sunlight's Congress API
"""
__author__ = "Chris Amico (eyeseast@gmail.com)"
__version__ = "0.1.2"
__copyright__ = "Copyright (c) 2010 Chris Amico"
__license__ = "MIT"

import os
import urllib
import httplib2
try:
    import json
except ImportError:
    import simplejson as json

__all__ = ['SunlightError', 'Sunlight']

BASE_URL = "http://services.sunlightlabs.com/api/%s.json?%s"

RESPONSE_KEYS = {
    # simple keys to skip the level we already know

    'legislators.get':                  lambda r: r['legislator'],
    'legislators.getList':              lambda r: [d['legislator'] for d in r['legislators']],
    'legislators.search':               lambda r: r['results'],
    'legislators.allForZip':            lambda r: [d['legislator'] for d in r['legislators']],
    'legislators.allForLatLong':        lambda r: [d['legislator'] for d in r['legislators']],

    'districts.getDistrictsFromZip':    lambda r: [d['district'] for d in r['districts']],
    'districts.getZipsFromDistrict':    lambda r: r['zips'],
    'districts.getDistrictFromLatLong': lambda r: [d['district'] for d in r['districts']],
    
    'committees.getList':               lambda r: [d['committee'] for d in r['committees']],
    'committees.get':                   lambda r: r['committee'],
    'committees.allForLegislator':      lambda r: [d['committee'] for d in r['committees']],
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
    def __init__(self, apikey=None, method=None, cache='.cache'):
        self.apikey = apikey or os.environ.get('SUNLIGHT_API_KEY', '')
        self.cache = cache
        self.http = httplib2.Http(cache)
        self.method = method
    
    def __getattr__(self, method):
        if self.method:
            return Sunlight(self.apikey, "%s.%s" % (self.method, method), self.cache)
        else:
            return Sunlight(self.apikey, method, self.cache)
    
    def __call__(self, **params):
        params['apikey'] = self.apikey
        url = BASE_URL % (self.method, urllib.urlencode(params))
        try:
            resp, content = self.http.request(url)
        except Exception, e:
            raise SunlightError(e)
        
        content = json.loads(content)
        parse = RESPONSE_KEYS.get(self.method)
        if callable(parse):
            content = parse(content['response'])
        
        return content
    
    def __repr__(self):
        return "<Sunlight: %s>" % self.method
