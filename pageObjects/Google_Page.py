'''
Created on Mar 16, 2016

@author: Anukul.Singhal
'''

from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
#from selenium.webdriver.firefox.webdriver import WebDriver
    
def textfield_Search(dr):
    dr.wait = WebDriverWait(dr, 30)
    try:
        element = dr.wait.until(EC.presence_of_element_located((By.NAME, "q"))) 
    except TimeoutException:
        print("Search text field not found in google.com")    
    return element
#end textfield_Search

def button_Search(dr):
    dr.wait = WebDriverWait(dr, 30)
    try:
        element = dr.wait.until(EC.element_to_be_clickable((By.NAME, "btnG"))) 
    except TimeoutException:
        print("Search button not found in google.com")    
    return element
#end button_Search
    
def link_Selenium(dr):
    dr.wait = WebDriverWait(dr, 30)
    try:
        element = dr.wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Selenium WebDriver")))
    except Exception, e:
        print "Element not found :", e
    return element
#end link_Selenium
    
def body_SeleniumPage(dr):
    dr.wait = WebDriverWait(dr, 30)
    try:
        dr.wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Browser Automation")))
    except Exception, e:
        print "Unable to fetch Selenium page source:", e
    return dr.page_source
#end body_SeleniumPage
    