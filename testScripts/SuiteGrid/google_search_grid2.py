import unittest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from projectModule import Google_Actions
from utility import Common_Actions
from utility import TestData_Loader
from utility.ParameterizedTestCase import ParameterizedTestCase

'''
    For all grid related scripts, need to inherit class from ParameterizedTestCase (instead of unittest.TestCase) in order
    to access variables like browser, ip and port on which to execute remote webdriver
'''
class Google_Search(ParameterizedTestCase):
    
    def setUp(self):
        print "executing from Suite Grid..."
        remote_webdriver_params = self.param
#         print "param is:", remote_webdriver_params
#         browser = remote_webdriver_params[2]
#         ip = remote_webdriver_params[0]
#         port = remote_webdriver_params[1]
#         if browser == "firefox":
#             cap = DesiredCapabilities.FIREFOX
#         
#         remote_url = "http://" + ip + ":" + str(port) + "/wd/hub"
#         print "remote url is:", remote_url
        
        this = self.__class__
        self.data = TestData_Loader.loadTestData(this)
        url = self.data.getCellData(this, "URL")
#         self.driver = webdriver.Remote(
#                         command_executor='http://127.0.0.1:4444/wd/hub',
#                         desired_capabilities=DesiredCapabilities.FIREFOX
#                     )
        
#         self.driver = webdriver.Remote(
#                         command_executor=remote_url,
#                         desired_capabilities=cap
#                     )

        self.driver = Common_Actions.openRemoteBrowser(remote_webdriver_params)
        self.driver.get(url)  
    
    def test_google_search(self):
        driver = self.driver
        this = self.__class__
        search_str = self.data.getCellData(this, "Search_String")
        Google_Actions.googleSearch(driver, search_str)               
        
    def tearDown(self):
        self.driver.close()