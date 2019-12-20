from CampScanner import CampScanner
from FacilityIDsFinder import FacilityIDsFinder
from Notifier import Notifier
import time

if __name__ == "__main__":

    ''' 
    Parameters for FacilityIDsFinder. It is recommended that keywords be supplied
    for best results. If the API fails to retrieve a facility, the facility id can always be found
    by going directly to the campground webpage where the 6 digit number at the end of the URL is the facility id 
    '''
    
    apiKey = "your api key here"
    facilityName = "Jumbo Rocks Campground"
    keywords = "Joshua Tree National Park, desert, hiking"
    state = "CA"
    idx = None

    jRocksCamp = FacilityIDsFinder(apiKey, facilityName, keywords, state, idx)
    
    # parameters to the scanner
    facilityID = jRocksCamp.getFacilityID()
    startDate = "01/05/2020"
    endDate = "01/07/2020"

    scanner = CampScanner(facilityID, startDate, endDate)
    
    # keep scanning until an available campsite is found. 
    while(True):
        scanner.scanCampground()
        if scanner.getAvailableCampSites():
            break
        time.sleep(900) # wait 900 secs/15 mins before scanning again

    # parameters to Notifier
    password = "password1234" # put sending email password here
    sEmailAddr = "example@email.com" # sending email address here
    rEmailAddr = "recexample@email.com" # receiving email address to send to here
    subject = "Available Sites!"
    emailMsgBdy = ("Campsites are available at " + facilityName + ". Navigate to " 
    "https://www.recreation.gov/camping/campgrounds/" + facilityID + "/availability"
    " to view the availability table.")
    
    notifier = Notifier(password, sEmailAddr, rEmailAddr, subject, emailMsgBdy)
    notifier.buildMessage()
    notifier.send()


