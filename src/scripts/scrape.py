from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import contextlib
import selenium.webdriver as webdriver
import selenium.webdriver.support.ui as ui
import time
from datetime import date
import random

def initialize_driver(url):
    driver = webdriver.Chrome()
    driver.get(url)
    return driver
def kill_driver(driver):
    driver.quit()
    return True
def change_url(driver,new_url):
    driver.get(new_url)
    return driver
def search_by_xpath(driver,xpath):
    lists = driver.find_elements_by_xpath(xpath)
    return lists
    
def initialize(company_name_actual,company_name):
    driver = webdriver.Chrome()
    url = "https://craft.co/search?layout=list&order=relevance&q=curr_search&locations%5B0%5D=US"
    curr_url = url.replace("curr_search",company_name)
    driver.get(curr_url)
    time_sleep =  random.randint(1,5)
    view_companies = driver.find_elements_by_xpath("//a[contains(text(),'View company')]")
    best_match = view_companies[0].get_attribute("href")
    driver.get(best_match)
    return best_match,driver
    
def scrape(company_name_actual,company_name,ranking):
    url,driver = initialize(company_name_actual,company_name)
    HQ = get_HQ(driver)
    employee_num = get_employee_num(driver)
    website = get_website(driver)
    company_name_on_this_page = get_company_name(driver)
    summary_tags = get_summary_tags(driver)
    description = get_description(driver)
    date_string = date.today().strftime("%d/%m/%Y")
    
    list_to_return = [company_name_on_this_page,ranking,url,website,HQ,summary_tags,employee_num,description,dateString]
    
    
def get_description(driver):
    try:
        description = driver.find_element_by_xpath("//meta[@name='description']").get_attribute("content")
    except:
        description = "Unknown"
    return description
                                   
def get_HQ(driver):
    try:
        HQ = driver.find_element_by_xpath("//tr//td[contains(text(),'HQ')]/following-sibling::td").text
    except:
        HQ = "Unknown"
    return HQ

def get_employee_num(driver):
    try:
        employee_num = driver.find_element_by_xpath("//tr//td[contains(text(),'Employees ')]/following-sibling::td").text
    except:
        employee_num = np.nan
    return employee_num

def get_website(driver):
    try:
        website = driver.find_element_by_xpath("//tr//td[contains(text(),'Website')]/following-sibling::td").text
    except:
        website = "Unknown"
    return website



def get_company_name(driver):
    try:
        company_name = driver.find_element_by_xpath("//h1[@class='summary__company-name']").text
    except:
        company_name = "Unknown"
    return company_name


def get_summary_tags(driver):
    try:
        summary_tags = driver.find_elements_by_xpath("//ul[@class='summary__tags']//li[@class='summary__tag']//a")
        summary_tags = [tag.text for tag in summary_tags]
    except:
        summary_tags = []
    return summary_tags

