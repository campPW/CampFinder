import json
import sys
import requests

class FacilityIDsFinder:
    # constructor takes a facility name, a comma delimited string of keywords (pass None if not using keywords), the 
    # two character code for the state (e.g., CA), and an optional positional index of
    # facility if the program was already ran and returned multiple facilities
    def __init__(self, apiKey, facilityName, keywords, stateCode, jsonIdx):
        self._facilityName = facilityName 
        self._keywords = "," + str(keywords) # convert to string in the event 'None' keyword was passed
        self._RIDB_API_URL = "https://ridb.recreation.gov/api/v1/facilities"
        self._RIDB_API_KEY = apiKey
        self._stateCode = stateCode
        self._jsonIdx = jsonIdx
        self._RIDB_API_PAYLOAD = {'query': self._facilityName + self._keywords, 'limit': 3, 'offset' : 0,
         'state': self._stateCode, 'full': "false", 'apikey': self._RIDB_API_KEY}
        self._facilityID = self._findFacilityID()
    
    def getFacilityID(self):
        return self._facilityID

    def getFacilityName(self):
        return self._facilityName 

    def _findFacilityID(self):
        response = requests.get(self._RIDB_API_URL, params=self._RIDB_API_PAYLOAD)
        responseStr = response.text
        parsedJson = json.loads(responseStr)
        
        # check if index was specified
        if self._jsonIdx == None:
            # check that the list is not empty
            if len(parsedJson['RECDATA']) == 0:
                print("The API failed to return any campsites using the given search parameters")
                sys.exit()
            elif len(parsedJson['RECDATA']) > 1:
                print("More than one facility found: ")
                # if the API call returna more than a single facility, print
                # the facility names andaexit the program
                for index, f in enumerate(parsedJson['RECDATA']):
                    print("Index " + str(index) + ": " + "".join(f['FacilityName']))

                print("Note the index of the desired facility and pass as argument to"
                    + " FacilityIDFinder constructor")
                sys.exit()
            # if the API does not return multiple sites or zero sites, and jsonIdx is null, grab the single facility ID
            elif not self._jsonIdx:
                fID = (parsedJson['RECDATA'][0]['FacilityID']) 
        # if index was specified, just grab the ID of the facility at that index
        else:
            fID = (parsedJson['RECDATA'][self._jsonIdx]['FacilityID']) 
        return fID
        
    def _findCampsiteID(self, facilityID, siteNumber):

        siteAPIURL = self._RIDB_API_URL + "/" + facilityID + "/campsites"
        self._RIDB_API_PAYLOAD['query'] = siteNumber
            
        response = requests.get(siteAPIURL, params=self._RIDB_API_PAYLOAD)
        responseStr = response.text
        parsedJson = json.loads(responseStr)

        campsiteID = parsedJson['RECDATA'][0]['CampsiteID']
        
        return campsiteID

    def getCampsiteID(self, siteNum):
        cID = self._findCampsiteID(self._facilityID, siteNum)
        return cID
        

            
    

        
