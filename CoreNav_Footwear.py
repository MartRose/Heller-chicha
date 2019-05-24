#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from __builtin__ import file
import ConfigParser
import unittest, time, re, os
import subprocess

from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.remote.errorhandler import ErrorHandler
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.events import AbstractEventListener
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains


env =    "qa" ##prod/dev/qa
site = "soccer" ##soccer/431/wss/wrs
device = "desktop"  ### Will be used once we move to mobile testing
grid =   "10.159.101.69"  ### IP address of the GRID server
clubSearch = 'carolina rapids'  ### Not used in this script but more of a placeholder
clubLink = 'CAROLINA RAPIDS'  ### Not used in this script but more of a placeholder

if site == "soccer":
    if env == "prod"  : base_url = "https://www.soccer.com"
    elif env == "dev" : base_url = "https://dx-dev-soc.sportsendeavors.net"
    else: base_url = "https://dx-qa-soc.sportsendeavors.net"
elif site == "431":
    if env == "prod"  : base_url = "https://www.431sports.com"
    elif env == "dev" : base_url = "https://dx-dev-431.sportsendeavors.net"
    else: base_url = "https://dx-qa-431.sportsendeavors.net"
elif site == "wss":
    if env == "prod"  : base_url = "https://www.worldsoccershop.com"
    elif env == "dev" : base_url = "https://qas-wss.sportsendeavors.net"
    else: base_url = "https://qa2-wss.sportsendeavors.net"
elif site == "wrs":
    if env == "prod"  : base_url = "https://www.worldrugbyshop.com"
    elif env == "dev" : base_url = "https://qas-wrs.sportsendeavors.net"
    else: base_url = "https://qa2-wrs.sportsendeavors.net"
else :
    print ("Please enter a valid site/environment option")
    print ("You've entered: " + site + " & " + env)
    exit()
###############################################
#Variables                                   ##
################################################
timestamp = time.strftime('%m-%d-%Y_%H-%M-%S')

################################################

################################################
#Menu                                         ##
################################################
print ("\n" * 10)
print "########################################################################################"
print ("SEI Core Nav Footwear")
print ("GRID IP:                          " + grid)
print ("Link to Live Preview:             http://" + grid +":4444/grid/admin/live?refresh=30")
print ("Website Page to be scraped:       " + base_url)
print ("Log Location:                     logs/"+site+"_links_" + timestamp + ".log")
print "########################################################################################"

################################################        
#Selenium Setup                               ##
################################################
class TC(unittest.TestCase):   ##this block puts on the grid
    def setUp(self):
        self.driver = webdriver.Remote(
        command_executor='http://' + grid + ':4444/wd/hub',
            desired_capabilities={
            'browserName': 'chrome',
            'name': ''+site+'CoreNav_Footwear'+timestamp+'', #Update this to reflect the test case name
            'screenResolution': '1920x1080',
            'tz': 'America/New_York',
            'acceptSslCerts': 'True',
                })
        self.driver.set_window_size(1920, 1080)
        self.driver.implicitly_wait(120)
        self.verificationErrors = []
        self.accept_next_alert = True
        self.driver

    def test_link_t_c(self):
        ###############################################################################
        #Config driver, open base url page and set zalenium cookie
        ###############################################################################
        driver = self.driver
        driver.maximize_window()
        driver.get(base_url)
        print ("Opened page: " + base_url)
        self.driver.add_cookie({'name' : 'zaleniumTestPassed', 'value' : 'false'})
        ###############################################################################
        #Scrape page for all links and create list, remove known non-valid links
        ###############################################################################
        Footwear_link = []
    
        actions = ActionChains(driver)
        Main_Footwear = driver.find_element_by_id("core-nav-primary")
        actions.move_to_element(Main_Footwear).perform();
        content_blocks = driver.find_elements_by_id("7614f102-c778-401f-a5fe-b4b247b89527")
        for block in content_blocks:
            FWlinks = block.find_elements_by_tag_name("a")
            for el in FWlinks:
                Footwear_link.append(el.get_attribute('href'))
        for a in Footwear_link:
            if a.startswith(base_url):                                             
                driver.get(a)
                driver.set_page_load_timeout(100)
                if driver.current_url == a:
                    print("Successfully opened:" +a + "\n")
                else:
                    print("This page is not correct: " +a + "\n")    
                time.sleep(1)               
            else:
                print("This link is not correct for this environment: " +a)
                
            
        
        ###############################################################################
        #Return to base URL and set zalenium cookie
        ###############################################################################
        driver.get(base_url)
        self.driver.add_cookie({'name' : 'zaleniumTestPassed', 'value' : 'true'})


    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()





       

