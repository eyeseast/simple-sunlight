import unittest
import urllib2
from sunlight import Sunlight, SunlightError, json

class SunlightTest(unittest.TestCase):
    
    def setUp(self):
        self.sunlight = Sunlight('9a097f6d04afc2174e3946ab715cc6a2')
    
    def compare(self, url, query, response_key):
        control = json.load(urllib2.urlopen(url))['response'][response_key]
        self.assertEqual(control, query)
    
    def testMethod(self):
        sunlight = Sunlight('9a097f6d04afc2174e3946ab715cc6a2', 'legislators')
        self.assertEqual(sunlight.method, 'legislators')

class LegislatorTest(SunlightTest):

    def testCall(self):
        pelosi = self.sunlight.legislators.get(lastname='pelosi')
        self.assertEqual(pelosi['firstname'], 'Nancy')
        
    def testList(self):
        url = "http://services.sunlightlabs.com/api/legislators.getList?apikey=9a097f6d04afc2174e3946ab715cc6a2&state=AZ&title=Sen"
        self.compare(url, self.sunlight.legislators.getList(state='AZ', title='Sen'), 'legislators')

class DistrictTest(SunlightTest):
    
    def testGet(self):
        pass
    
    def testList(self):
        pass

class CommitteeTest(SunlightTest):
    
    def testGet(self):
        url = "http://services.sunlightlabs.com/api/committees.get?apikey=9a097f6d04afc2174e3946ab715cc6a2&id=SSEV_grn"
        query = self.sunlight.committees.get(id='SSEV_grn')
        self.compare(url, query, 'committee')
        
    def testList(self):
        url = "http://services.sunlightlabs.com/api/committees.getList?chamber=Senate&apikey=9a097f6d04afc2174e3946ab715cc6a2"
        query = self.sunlight.committees.getList(chamber='Senate')
        self.compare(url, query, 'committees')

if __name__ == '__main__':
    unittest.main()