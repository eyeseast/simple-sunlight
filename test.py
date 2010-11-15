#!/usr/bin/env python
import os
import unittest
import urllib2
from sunlight import Sunlight, SunlightError, json

API_KEY = os.environ.get('SUNLIGHT_API_KEY', '')

class SunlightTest(unittest.TestCase):
    
    def setUp(self):
        self.sunlight = Sunlight(API_KEY)
    
    def compare(self, url, query, parse):
        control = parse(json.load(urllib2.urlopen(url))['response'])
        self.assertEqual(control, query)

class ClientTest(SunlightTest):
    
    def testMethod(self):
        sunlight = Sunlight(API_KEY, 'legislators')
        self.assertEqual(sunlight.method, 'legislators')

class LegislatorTest(SunlightTest):

    def testCall(self):
        pelosi = self.sunlight.legislators.get(lastname='pelosi')
        self.assertEqual(pelosi['firstname'], 'Nancy')
        
    def testList(self):
        url = "http://services.sunlightlabs.com/api/legislators.getList?apikey=%s&state=AZ&title=Sen" % API_KEY
        self.compare(url, self.sunlight.legislators.getList(state='AZ', title='Sen'), 
            lambda r: [r['legislator'] for r in r['legislators']])

class DistrictTest(SunlightTest):
    
    def testGetFromZip(self):
        url = "http://services.sunlightlabs.com/api/districts.getDistrictsFromZip?apikey=%s&zip=91355" % API_KEY
        query = self.sunlight.districts.getDistrictsFromZip(zip=91355)
        self.compare(url, query, lambda r: [r['district'] for r in r['districts']])
    
    def testLatLong(self):
        url = "http://services.sunlightlabs.com/api/districts.getDistrictFromLatLong.json?latitude=35.778788&longitude=-78.787805&apikey=%s" % API_KEY
        query = self.sunlight.districts.getDistrictFromLatLong(latitude=35.778788, longitude=-78.787805)
        self.compare(url, query, lambda r: [r['district'] for r in r['districts']])

class CommitteeTest(SunlightTest):
    
    def testGet(self):
        url = "http://services.sunlightlabs.com/api/committees.get?apikey=%s&id=SSEV_grn" % API_KEY
        query = self.sunlight.committees.get(id='SSEV_grn')
        self.compare(url, query, lambda r: r['committee'])
        
    def testList(self):
        url = "http://services.sunlightlabs.com/api/committees.getList?chamber=Senate&apikey=%s" % API_KEY
        query = self.sunlight.committees.getList(chamber='Senate')
        self.compare(url, query, lambda r: [r['committee'] for r in r['committees']])

if __name__ == '__main__':
    unittest.main()