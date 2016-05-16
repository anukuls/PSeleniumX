import unittest
from selenium import webdriver
from projectModule import Google_Actions
from utility import Common_Actions, Reporter
from utility import TestData_Loader
import utility.Reporter

class Google_Search(unittest.TestCase):
    
    def setUp(self):
        browser = Common_Actions.getBrowserFromConfig()
        this = self.__class__
        self.data = TestData_Loader.loadTestData(this)
        url = self.data.getCellData(this, "URL")
        self.driver = Common_Actions.openBrowser(browser)
        self.driver.get(url) 
        Reporter.addTestStepDetail("Successfully navigated to URL : %s" % url)
    
    def test_google_search(self):
        driver = self.driver
        this = self.__class__
        search_str = self.data.getCellData(this, "Search_String")
        Google_Actions.googleSearch(driver, search_str)               
        
    def tearDown(self):
        self.driver.close()