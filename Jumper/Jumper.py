import json
from selenium import webdriver
from Jumper import Crawler
"""
JSON FILE
Type : FIND
    Summary -> find the pages with keywords in given URL
    URL : given URL
    keywords : given keywords 
"""

def Processor(data) :
    """
    Query = json.loads(data)
    if Query["Type"]=="FIND" :
        a = Crawler()
    """
    slave = Crawler.Crawler(data)

    """
        New query Here
    """

print("Hi I'm new slave")
