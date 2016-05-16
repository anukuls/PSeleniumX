import unittest
from selenium import webdriver
from projectModule import Google_Actions
from utility import Common_Actions
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
    
    def test_google_search(self):
        driver = self.driver
        this = self.__class__
        search_str = self.data.getCellData(this, "Search_String")
        Google_Actions.googleSearch(driver, search_str)               
        
    def tearDown(self):
        self.driver.close()
        
# if __name__ == "__main__":
#     unittest.main()
            
# test_case = Google_Search()
# test_case.main()
# test_case.postScript()
#         

# def suite():
#     """
#         Gather all the tests from this module in a test suite.
#     """
#     test_suite = unittest.TestSuite()
#     test_suite.addTest(unittest.makeSuite(Google_Search))
#     return test_suite
# 
# mySuit=suite()
# 
# 
# runner=unittest.TextTestRunner()
# runner.run(mySuit)