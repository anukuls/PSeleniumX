from selenium import webdriver
from pageObjects import Google_Page
from time import sleep
  
def googleSearch(drvr, search_txt):
    Google_Page.textfield_Search(drvr).send_keys(search_txt)
    Google_Page.button_Search(drvr).click()
    Google_Page.link_Selenium(drvr).click()
    assert "Selenium is a suite of tools" in Google_Page.body_SeleniumPage(drvr)
#end googleSearch