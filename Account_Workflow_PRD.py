#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver import chrome 
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.support.events import AbstractEventListener
from selenium import webdriver
from selenium.webdriver.remote.errorhandler import ErrorHandler
from selenium.webdriver.common.action_chains import ActionChains
import sys
import ConfigParser
import unittest, time, re, os
import subprocess


################################################
#Variables                                   ## 
################################################
timestamp = time.strftime('%m-%d-%Y_%H-%M-%S')

################################################
#Import Config Info                           ##
################################################
config = ConfigParser.ConfigParser()
#dir = subprocess.check_output("pwd", shell=True)
#print (dir)
config.read("config.ini")
################################################
#Set Variables from Config File                ##
################################################
site = config.get('test_config','site')
env = "prod"
device = config.get('test_config','device')
grid =   config.get('test_config','grid')
#user = config.get('test_config', 'user')
#password = config.get('test_config', 'password')

if site == "soccer":
    if env == "prod"  : base_url = "https://www.soccer.com"
    elif env == "dev" : base_url = "https://dx-dev-soc.sportsendeavors.net/"
    else: base_url = "https://dx-qa-soc.sportsendeavors.net/"
elif site == "431":
    if env == "prod"  : base_url = "https://www.431sports.com"
    elif env == "dev" : base_url = "https://dx-dev-431.sportsendeavors.net/"
    else: base_url = "https://dx-qa-431.sportsendeavors.net/"
elif site == "wss":
    if env == "prod"  : base_url = "https://www.worldsoccershop.com/"
    elif env == "dev" : base_url = "https://qas-wss.sportsendeavors.net/"
    else: base_url = "https://qa2-wss.sportsendeavors.net/"
elif site == "wrs":
    if env == "prod"  : base_url = "https://www.worldrugbyshop.com/"
    elif env == "dev" : base_url = "https://qas-wrs.sportsendeavors.net/"
    else: base_url = "https://qa2-wrs.sportsendeavors.net/"
else :
    print ("Please enter a valid site/environment option")
    print ("You've entered: " + site + " & " + env)
    exit()
###############################################
#Variables                                   ##
################################################
timestamp = time.strftime('%m-%d-%Y_%H-%M-%S')
 
 
################################################
#Menu                                         ##
################################################
print ("\n" * 10)
print "########################################################################################"
#print ("Script Executed from directory " + dir)
print ("GRID IP:                          " + grid)
print ("Link to Live Preview:             http://" + grid +":4444/grid/admin/live?refresh=30")
print ("Website Page to be scraped:       " + base_url)
print ("Log Location:                     logs/"+site+"_Account_Workflow_PRD_" + timestamp + ".log")
print "########################################################################################"
 
 
 
################################################        
#Selenium Setup                               ##
################################################
class TC(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Remote(
        command_executor='http://' + grid + ':4444/wd/hub',
            desired_capabilities={
            'browserName': 'chrome',
            'name': ''+site+'_Account_Workflow_PRD_'+timestamp+'', #Update this to reflect the test case name
            'screenResolution': '1920x1080',
            'tz': 'America/New_York',
            'acceptSslCerts': 'True',
                })
        self.driver.set_window_size(1920, 1080)
        self.driver.implicitly_wait(120)
        self.verificationErrors = []
        self.accept_next_alert = True
        self.driver
 
 
 
    def test_case(self):
        ###############################################################################
        #Config driver, open base url page and set zalenium cookie
        ###############################################################################
        driver = self.driver
        driver.maximize_window()
        driver.get(base_url)
        print ("Opened page: " + base_url)
        self.driver.add_cookie({'name' : 'zaleniumTestPassed', 'value' : 'false'})
        ###############################################################################
        #Sign In
        self.driver.add_cookie({'name' : 'zaleniumMessage', 'value' : 'Signing in'})
        driver.find_element_by_link_text("Sign In").click()
        signin_blank = driver.find_element_by_name("email")
        signin_name = "essie226mayes@gmail.com"
        signin_blank.click()
        signin_blank.clear()
        for character in signin_name:
            signin_blank.send_keys(character)
            time.sleep(0.2)
        time.sleep(1)
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys("password123")
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Invalid Email Address and/or Password'])[1]/following::input[1]").click()
        driver.find_element_by_xpath("//button[contains(text(),'Individual Account')]").click()
        self.driver.add_cookie({'name' : 'zaleniumMessage', 'value' : 'Waiting for Goal Club drop down to close'})
        time.sleep(5)
        #Go to Account Information
        self.driver.add_cookie({'name' : 'zaleniumMessage', 'value' : 'Go to Account Information'})
        actions = ActionChains(driver)
        My_Account = driver.find_element_by_xpath("//div[@id='main-nav-account-wrapper']/div[2]/button/span")
        actions.move_to_element(My_Account).perform();
        time.sleep(2)
        Account_Information = driver.find_element_by_link_text("Account Information").click()
        time.sleep(10)
        #Change Preferences (Phone number) and Save 
        self.driver.add_cookie({'name' : 'zaleniumMessage', 'value' : 'Change Phone number and Save'})
        driver.find_element_by_xpath("//form[@id='account-form']/div[2]/div[2]/label/input").click()
        driver.find_element_by_xpath("//input[@id='phone1']").click()
        driver.find_element_by_xpath("//input[@id='phone1']").clear()
        driver.find_element_by_xpath("//input[@id='phone1']").send_keys("1232100")
        driver.find_element_by_xpath("//a[contains(text(),'Save')]").click()
        time.sleep(5)
        #Move to top of page
        self.driver.add_cookie({'name' : 'zaleniumMessage', 'value' : 'Moving to Top of Page'})
        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
        time.sleep(2)
        #Add New Address 
        self.driver.add_cookie({'name' : 'zaleniumMessage', 'value' : 'Adding a new Address'})  
        driver.find_element_by_xpath("//li[@class='tabs-title um-tabs-title']//a[@href='#addressBook'][contains(text(),'Address Book')]").click()
        driver.find_element_by_xpath("//a[contains(text(),'Add a new address')]").click()
        driver.find_element_by_name("firstName").click()
        driver.find_element_by_name("firstName").clear()
        driver.find_element_by_name("firstName").send_keys("Nelix")
        driver.find_element_by_name("lastName").click()
        driver.find_element_by_name("lastName").clear()
        driver.find_element_by_name("lastName").send_keys("Butterpath")
        driver.find_element_by_name("street").click()
        driver.find_element_by_name("street").clear()
        driver.find_element_by_name("street").send_keys("3005 W", " Kilbourn Ave")
        driver.find_element_by_name("zip").click()
        driver.find_element_by_name("zip").clear()
        driver.find_element_by_name("zip").send_keys("53208")
        driver.find_element_by_name("city").click()
        driver.find_element_by_name("city").clear()
        driver.find_element_by_name("city").send_keys("Milwaukee")
        driver.find_element_by_name("email").click()
        driver.find_element_by_name("email").clear()
        driver.find_element_by_name("email").send_keys("uripides.new@mailinator.com")
        driver.find_element_by_id("phone").click()
        driver.find_element_by_id("phone").clear()
        driver.find_element_by_id("phone").send_keys("121412316")
        driver.find_element_by_name("state").click()
        Select(driver.find_element_by_name("state")).select_by_visible_text("WISCONSIN")
        driver.find_element_by_name("state").click()
        time.sleep(2)
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='phone number is required'])[1]/following::a[1]").click()
        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
        driver.find_element_by_tag_name('body').send_keys(Keys.F5)
        time.sleep(5)
        #Edit/Save Registration Address
        self.driver.add_cookie({'name' : 'zaleniumMessage', 'value' : 'Edit Registration Address'})
        driver.find_element_by_xpath("//a[contains(text(),'Edit')]").click()
        reg_add_blank = driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Address'])[2]/following::input[1]")
        new_str_add = "6111 Estate Nazareth"
        reg_add_blank.click()
        reg_add_blank.clear()
        for character in new_str_add:
            reg_add_blank.send_keys(character)
            time.sleep(0.2)
        time.sleep(2)    
        driver.find_element_by_xpath("//div[@class='columns buttons']//a[@class='button'][contains(text(),'Save Address')]").click()
        driver.find_element_by_xpath("//div[@class='columns buttons']//a[@class='button'][contains(text(),'Save Address')]").click()
        time.sleep(2)
        #Check Order History
        self.driver.add_cookie({'name' : 'zaleniumMessage', 'value' : 'Checking Order History'})
        driver.find_element_by_xpath("//li[@class='tabs-title um-tabs-title']//a[@href='#orderHistory'][contains(text(),'My Orders')]").click()
        time.sleep(1)
        driver.find_element_by_xpath("//a[contains(text(),'+ View Order')]").click()
        time.sleep(5)
        driver.find_element_by_xpath("//a[contains(text(),'- View Order')]").click()
        time.sleep(1)
        ##Put everything back to rights###############################################
        self.driver.add_cookie({'name' : 'zaleniumMessage', 'value' : 'Putting Everything Back to Rights'})
        #Edit/Save Registration Address
        driver.find_element_by_xpath("//li[@class='tabs-title um-tabs-title']//a[@href='#addressBook'][contains(text(),'Address Book')]").click()
        driver.find_element_by_xpath("//a[contains(text(),'Edit')]").click()
        reg_add_blank = driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Address'])[2]/following::input[1]")
        old_str_add = "6281 Estate Nazareth"
        reg_add_blank.click()
        reg_add_blank.clear()
        for character in old_str_add:
            reg_add_blank.send_keys(character)
            time.sleep(0.2)
        self.driver.add_cookie({'name' : 'zaleniumMessage', 'value' : 'Changing address back'})
        time.sleep(0.5)
        driver.find_element_by_xpath("//div[@class='columns buttons']//a[@class='button'][contains(text(),'Save Address')]").click()
        driver.find_element_by_xpath("//div[@class='columns buttons']//a[@class='button'][contains(text(),'Save Address')]").click()
        time.sleep(2)
        #Remove Address
        self.driver.add_cookie({'name' : 'zaleniumMessage', 'value' : 'Removing the added address'})
        driver.find_element_by_xpath("//div[@class='tabs-content']//div[2]//p[5]//a[2]").click()
        time.sleep(2)
        #Change Preferences (Phone number) and Save 
        self.driver.add_cookie({'name' : 'zaleniumMessage', 'value' : 'Changing Phone Number back'})
        driver.find_element_by_xpath("//li[@class='tabs-title um-tabs-title']//a[@href='#userInfo'][contains(text(),'Account Overview')]").click()
        driver.find_element_by_xpath("//form[@id='account-form']/div[2]/div[2]/label/input").click()
        driver.find_element_by_xpath("//input[@id='phone1']").click()
        driver.find_element_by_xpath("//input[@id='phone1']").clear()
        driver.find_element_by_xpath("//input[@id='phone1']").send_keys("202-341232100")
        driver.find_element_by_xpath("//a[contains(text(),'Save')]").click()
        #Move to top of page
        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
        time.sleep(2)
        #Sign Out
        self.driver.add_cookie({'name' : 'zaleniumMessage', 'value' : 'Signing Out'})
        actions = ActionChains(driver)
        My_Account = driver.find_element_by_xpath("//div[@id='main-nav-account-wrapper']/div[2]/button/span")
        actions.move_to_element(My_Account).perform();
        time.sleep(2)
        Sign_Out = driver.find_element_by_link_text("Sign Out").click()
        self.driver.get(base_url)
        time.sleep(5)
        ###############################################################################
        #Return to base URL and set zalenium cookie
        ###############################################################################
        self.driver.get(base_url)
        self.driver.add_cookie({'name' : 'zaleniumTestPassed', 'value' : 'true'})
        print("Hey great! Your test ran!! with no errors!!")

    
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
        #self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
