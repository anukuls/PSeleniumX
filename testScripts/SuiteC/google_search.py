import unittest
from selenium import webdriver
from projectModule import Google_Actions
from utility import Common_Actions

class Google_Search(unittest.TestCase):
    
    def setUp(self):
        browser = Common_Actions.getBrowserFromConfig()
        self.driver = Common_Actions.openBrowser(browser) 
    
    def test_google_search(self):
        driver = self.driver
        driver.get("http://www.google.com")
        Google_Actions.googleSearch(driver, "Selenium WebDriver")               
        
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