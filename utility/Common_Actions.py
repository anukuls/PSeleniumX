import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from ConfigParser import SafeConfigParser
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging
import utility.Log_Manager

logger = logging.getLogger("utility.Common_Actions")

def openBrowser(browser_name):
    driver = None
    if browser_name == "firefox":
        logger.info("Launching Firefox Browser")
        driver = webdriver.Firefox()
    elif browser_name == "chrome":
        logger.info("Launching Chrome Browser")
        chromedriver = os.getcwd() + "\\..\\drivers\\chromedriver.exe"
        os.environ["webdriver.chrome.driver"] = chromedriver
        driver = webdriver.Chrome(chromedriver)
    elif browser_name == "ie":
        logger.info("Launching IE Browser")
    return driver
#end openBrowser

def getBrowserFromConfig():
    parser = SafeConfigParser()
    base_driver_config_path = os.getcwd() + "\\..\\config\\base_driver_config.ini"
    parser.read(base_driver_config_path)
    browser = parser.get('runConfig', 'browser')
    return browser

'''Add capabilitites for chrome and IE'''
def openRemoteBrowser(remote_params):
    browser = remote_params[2]
    ip = remote_params[0]
    port = remote_params[1]
    if browser == "firefox":
        cap = DesiredCapabilities.FIREFOX
    
    remote_url = "http://" + ip + ":" + str(port) + "/wd/hub"
    print "remote url is:", remote_url
    
    driver = webdriver.Remote(
                command_executor=remote_url,
                desired_capabilities=cap
            )
    return driver    