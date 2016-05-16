from selenium import webdriver
from pageObjects import Google_Page
from utility import Reporter
  
def googleSearch(drvr, search_txt):
    Google_Page.textfield_Search(drvr).send_keys(search_txt)
    Google_Page.button_Search(drvr).click()
    Reporter.addTestStepDetail("Successfully searched for %s text" % search_txt)
    Google_Page.link_Selenium(drvr).click()
    assert "Selenium is a suite of tools" in Google_Page.body_SeleniumPage(drvr)
    Reporter.addTestStepDetail("Successfully landed at Selenium Webdriver website")
#end googleSearch