import json
import requests

class FacilityIDFinder:

    def __init__(self, campgroundName):
        self._campgroundName = campgroundName
        self._RIDB_API_URL = "https://ridb.recreation.gov/api/v1/facilities"
        self._RIDB_API_KEY = "fda71395-e44c-4ee7-b0d2-acce1f07afc8"
        self._RIDB_API_PAYLOAD = {'query': self.campgroundName,'limit': 3, 'offset' : 0,
         'apikey': self.RIDB_API_KEY}
        self._facilityID = self.findFacilityID()
    
    def getFacilityID(self):
        return self.facilityID

    def findFacilityID(self):
        response = requests.get(self.RIDB_API_URL, params=self.RIDB_API_PAYLOAD)
        responseStr = response.text
        parsedJson = json.loads(responseStr)
        fID = (parsedJson['RECDATA'][0]['FacilityID'])
        return fID