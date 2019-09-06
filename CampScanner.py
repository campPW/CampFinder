from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import datetime
import time
import re

class CampScanner:

    def __init__(self, facilityID, startDate, endDate):
        self._BASE_URL = "https://www.recreation.gov/camping/campgrounds/"
        self._facilityID = facilityID
        self._startDate = startDate
        self._endDate = endDate
        self._endDateTimeObj = self._convertStrDate(self._endDate)
        self._startDateTimeObj = self._convertStrDate(self._startDate)
        self._availableCampsites = list()

    # scans through campsites in 10 day date range
    # TODO: add ability to scan for longer date ranges. Would need to automate browser to
    # click 'next 5 days' element
    
    def scan(self):
        # check that dates entered are valid
        today = datetime.date.today()

        if today > self._startDateTimeObj:
            raise ValueError("Invalid start date. Date cannot be less than current date ")
        elif self._startDateTimeObj == self._endDateTimeObj:
            raise ValueError("Check-out date cannot be the same as check-in date ")

        webDriver = self._setUpDriver()
        html = webDriver.page_source 
        webDriver.quit()
        soup = BeautifulSoup(html, 'html.parser')
        availSites = soup.find_all("td", "available")
        
        # iterate through each button returned by BeautifulSoup that represents
        #  an available site and parse out the site info (date & site number) 
        for site in availSites:
            s = site.find('button')
            ariaLabelStr = str(s)
            siteDict = ariaLabelStr.split('"')

            availDate = self._convertLabel(siteDict[1])            
            isValidDate = self._checkDateRange(availDate, self._startDateTimeObj, self._endDateTimeObj)
            
            if isValidDate == True:
                self._availableCampsites.append(siteDict[1]) # index 1 holds the data we want
            
    def _setUpDriver(self):
        driver = webdriver.Firefox()
        # check if user entered a date range. If they did, automate entry of those
        # dates and search for available spots
        if self._startDate != None and self._endDate != None:
            driver.get(self._BASE_URL + self._facilityID)
            
            startDateElem = driver.find_element_by_id("startDate")
            endDateElem = driver.find_element_by_id("endDate")
            viewByAvailElem = driver.find_element_by_id("campground-view-by-avail")

            actions = ActionChains(driver)
            actions.send_keys_to_element(startDateElem, self._startDate)
            actions.send_keys_to_element(endDateElem, self._endDate)
            actions.click(viewByAvailElem)
            actions.perform()

        # if no date range was entered, simply return default page, which displays
        # availability from current date forward    
            driver.get(self._BASE_URL + self._facilityID + "/availability")

        # wait until the availability table is present before returning the driver
        try:
            elem = WebDriverWait(driver, 25).until(EC.presence_of_element_located(
                By.CLASS_NAME, "camp-sortable-contents"))
        finally:
            return driver

    def _checkDateRange(self, availDate, startDate, endDate):
        # check that the date is not less than or greater than the start and
        # end date
        if availDate >= startDate and availDate <= endDate:
            return True
        else:
            return False

    # parse the availabilty date out of the aria-label string in html
    # and convert into a datetime object
    def _convertLabel(self, label):
        sl = re.split('\W+', label)
        month = int(self._monthToNum(sl[0]))
        day = int(sl[1])
        year = int(sl[2])
        convertedDate = datetime.date(year, month, day)
        return convertedDate

    # convert start or end date to a datetime object
    def _convertStrDate(self, date):
        sd = date.split('/')
        month = int(sd[0])
        day = int(sd[1])
        year = int(sd[2])
        convertedDate = datetime.date(year, month, day)
        return convertedDate

    def _monthToNum(self, month):
        switch = {
            "Jan" : 1,
            "Feb" : 2,
            "Mar" : 3,
            "Apr" : 4,
            "May" : 5,
            "Jun" : 6,
            "Jul" : 7,
            "Aug" : 8,
            "Sep" : 9,
            "Oct" : 10,
            "Nov" : 11,
            "Dec" : 12,
        }
        return switch.get(month, 0) # if 0 is returned, month is invalid
   
    def getAvailableCampSites(self):
        return self._availableCampsites
    def getEndDate(self):
        return self._endDateTimeObj

