"""
A really simple wrapper for Sunlight's Congress API
"""
__author__ = "Chris Amico (eyeseast@gmail.com)"
__version__ = "0.1.3"
__copyright__ = "Copyright (c) 2010 Chris Amico"
__license__ = "MIT"

# ## Simple Sunlight 
# 
# A Python client for the Sunlight Foundation's
# [Congress API](http://services.sunlightlabs.com/docs/Sunlight_Congress_API/).
# It returns JSON with fat trimmed. What you do with that is up to you.
# It should stay out of your way.

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
    # Responses come back with metadata we don't need,
    # so we trim fat where we can.

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

# A basic error subclass for anything that goes wrong
class SunlightError(Exception):
    "Exception for Sunlight API"

# The main **Sunlight** class handles methods and arguments
# in a way that still feels like Python.

class Sunlight(object):
    """
    A really simple Sunlight API client that just returns JSON
    
    Instantiate a Sunlight object with your API key:
    
    >>> sunlight = Sunlight(API_KEY)
    >>> pelosi = sunlight.legislators.get(lastname='pelosi')
    >>> print pelosi['firstname']
    Nancy
    """
    # Instantiate a Sunlight object with your API key: 
    def __init__(self, apikey=None, method=None, cache='.cache'):
        self.apikey = apikey or os.environ.get('SUNLIGHT_API_KEY', '')
        self.method = method
        
        # Caching is pluggable. Pass in memcache and httplib2
        # will use that instead of filesystem caching.
        # See [httplib2](http://httplib2.googlecode.com/hg/doc/html/libhttplib2.html#id2)
        # docs for more on pluggable caching.
        self.cache = cache
        self.http = httplib2.Http(cache)
    
    # Namespaces are defined on the fly. Ask for an arbitrary
    # method and Sunlight will tack it on. For example:
    # 
    #     >>> sunlight = Sunlight(API_KEY)
    #     >>> sunlght.foo
    #     <Sunlight: foo>
    #     >>> sunlight.foo.bar
    #     <Sunlight: foo.bar>
    def __getattr__(self, method):
        if self.method:
            return Sunlight(self.apikey, "%s.%s" % (self.method, method), self.cache)
        else:
            return Sunlight(self.apikey, method, self.cache)
    
    # Calling any attribute (as defined above) puts everything
    # together and makes the actual API call. Read the API documentation
    # at [Sunlight](http://services.sunlightlabs.com/docs/Sunlight_Congress_API/)
    # for specific arguments.
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
