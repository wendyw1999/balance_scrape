from src.etl.etl import *
from src.scripts.scrape import *

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
from difflib import SequenceMatcher
import pandas as pd
import numpy as np
import string
import re


def main():
    companies,companies_transformed = get_list_of_company_names("/data/company.txt")
    result_df = pd.DataFrame(columns = ["companyName","ranking","craftWebsite","companyWebsite","tags",
                             "HQ","employeeNumber","description","dateString"])
    for company in range(0,501):
        try:
            info_list = scrape(companies[company],companies_transformed[company],company+1)
            result_df.loc[len(result_df)] = info_list
            result_df.to_csv("/data/result_company_info.csv")
        except:
            print("Needs to look into:"+companies[company])
        
    