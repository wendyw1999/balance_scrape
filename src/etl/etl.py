from difflib import SequenceMatcher
import pandas as pd
import numpy as np
import string
import re

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