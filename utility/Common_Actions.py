import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from ConfigParser import SafeConfigParser
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def openBrowser(browser_name):
    driver = None
    if browser_name == "firefox":
        driver = webdriver.Firefox()
    elif browser_name == "chrome":
        print "starting chrome browser..."
        chromedriver = os.getcwd() + "\\..\\drivers\\chromedriver.exe"
        os.environ["webdriver.chrome.driver"] = chromedriver
        driver = webdriver.Chrome(chromedriver)
    elif browser_name == "ie":
        print "starting ie browser..."
    return driver
#end openBrowser

def getBrowserFromConfig():
    parser = SafeConfigParser()
    base_driver_config_path = os.getcwd() + "\\..\\config\\base_driver_config.ini"
    parser.read(base_driver_config_path)
    browser = parser.get('runConfig', 'browser')
    return browser

def openRemoteBrowser(remote_params):
    print "param is:", remote_params
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