from difflib import SequenceMatcher
import pandas as pd
import numpy as np
import string
import re

import xlsxwriter
import ethnicolr
import pandas as pd
import gender_guesser.detector as gender
import numpy as np
import requests
import os
from datetime import date
import time
from google.oauth2.service_account import Credentials
import gspread
from keras.models import load_model

## download images
def download_image_from_url(url,folder_location,name):
    '''
    url: the destination url of the image
    name: filename of the image to be stored, before the dot jpg
    folder_location: local file path of the image to be stored. e.g. data/test_data/
    '''
    extension = url.split(".")[-1]
    filename = folder_location+name+"."+extension
    
    urllib.request.urlretrieve(url, filename)
    return filename

# 
def guess_genders_races(names):
    '''
    names: a list of names of the people to be scraped
    returns: two lists, genders of the names, and races of the names
    '''
    df = pd.DataFrame({"name":names})
    df["name"] = df["name"].apply(lambda x:x.split(",")[0])

    df["last_name"] = df["name"].apply(lambda x:x.split(" ")[-1])
    df["first_name"] = df["name"].apply(lambda x:x.split(" ")[0])
    try:
        df2 = ethnicolr.census_ln(df,"last_name").set_index("last_name").drop(["name","first_name"],axis = 1)
    except:
        print(df2)
    df2["Unknown"] = 0
    df2 = df2.replace("(S)",0)
    import numpy as np
    df2["Unknown"] = df2["pctwhite"].isna().replace({False:0,True:100})
    df2.fillna(0)
    for column in df2.columns:
        df2[column] = pd.to_numeric(df2[column])
    races_df = df2.idxmax(axis="columns").replace({"pctwhite":"White","pctblack":"Black","pctapi":"Asian","pctaian":"Indian","pct2prace":"mixed",
                                       "pcthispanic":"hispanic"})
    #poc = (races_df == "White").replace({True:"White",False:"POC"}).values



    d = gender.Detector()
    genders = df["first_name"].apply(lambda x:d.get_gender(x)).replace({"male":"Male","female":"Female",
                                                                        "mostly_male":"Male",
                                                                        "mostly_female":"Female"}).values
    return genders,races_df.values



# Write to google worksheets
def write_to_worksheet(csv_filename,crendential_jsonpath,spreadsheet_name,sharing_google_emails):
    '''
    csv_filename: the path + filename of the csv to be sent as a worksheet
    spreadsheet_name: user defined new name of the google spreadsheet
    crendential_jsonpath: path+filename of the google credentials (don't show it publicly, acquired using google cloud platform tool)
    sharing_google_emails: a list of emails (have to be gmails) to be shared as we created the spreadsheet (editors)
    '''
    scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
    ]

    credentials = Credentials.from_service_account_file(
        crendential_jsonpath,
        scopes=scopes
    )
    gc = gspread.authorize(credentials)
    content = open(csv_filename, 'rb').read()
    sh = gc.create(spreadsheet_name)
    gc.import_csv(sh.id, content)
    print("Created new spreadsheet:"+spreadsheet_name+" From:"+csv_filename)
    for gmail in sharing_google_emails:
        sh.share(gmail, perm_type='user', role='writer')
        print("Sent to "+ gmail)
def write_to_csv(df, csv_filename):
    df.to_csv(csv_filename)
    return True
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def transform_text(company_name):
    # transform a company's name to feed into the url, removing all the punctuations replaced with search key ('%20')
    encoding_dict = {' ': '%20', ' & ': '%20', '!': '%21', '"': '%22', '#': '%23', '$': '%24', '%': '%25', '&': '%26', "'": '%27', '(': '%28', ')': '%29', '*': '%2A', '+': '%2B', ',': '%2C', '-': '%2D', '.': '%2E'}
    string1 = company_name
    string1 = string1.lower()
    for i in string1:
        if i in encoding_dict.keys():
            string1 = string1.replace(i,"%20")
    return string1

def get_list_of_company_names(path):
    df = pd.read_csv("company.txt",header=None)
    df.columns = ["company"]
    index = df.index
    companies = df["company"].values
    company_transformed = list(map(transform_text,companies))
    return companies,company_transformed