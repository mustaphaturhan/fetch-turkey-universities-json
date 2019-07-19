from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import re
# import pandas as pd
import os
import json
import io

# set variables
driver_path = "./geckodriver.exe"  # browser driver path / firefox in this case
url = "https://eyoksis.yok.gov.tr/websitesiuygulamalari/harita/"  # launch url
university_list = []  # create empty list for universities
output_file_name = 'universities.json'  # output file name

# create a new firefox session
options = Options()
options.headless = True  # launch firefox headless
driver = webdriver.Firefox(
    options=options, executable_path=driver_path)  # set driver
driver.implicitly_wait(1)
driver.get(url)  # go to url

# define class
class University(object):
    def __init__(self, name, phone, fax, web, email, address, warden):
        self.name = name
        self.phone = phone
        self.fax = fax
        self.web = web
        self.email = email
        self.address = address
        self.warden = warden

# define functions
def getElementText(afterPrefix):
    return driver.find_element_by_id(unique_id + afterPrefix).text  # get value


def appendUniversity():
    name = getElementText('4g-cap')  # get university name
    phone = getElementText('bg')  # get university phone
    fax = getElementText('jg')  # get university fax
    web = getElementText('rg')  # get university web
    email = getElementText('zg')  # get university email
    address = getElementText('6h')  # get university address
    warden = getElementText('eh')  # get university warden

    university_list.append(University(
        name, phone, fax, web, email, address, warden))  # append it to list

    close_button = driver.find_element_by_class_name(
        "z-window-close")  # find close university info window
    close_button.click()  # click it.


def goNextPage():
    try:
        nextButton = driver.find_element_by_class_name('z-paging-next') # find next button
    except:
        print('Cannot find next button.')
        driver.quit()

    nextButton.click() # click it

    try:
        isNextButtonDisabled = nextButton.get_attribute('disabled') # look for disabled attribute
        if isNextButtonDisabled == True: # if attribute is true
            print('Checked every page') # send a message
    except:
        addUniversitiesToList() # if there is no disabled attribute
        goNextPage() # go to the next page

# get unique id's prefix
try:
    wrapper = driver.find_element_by_class_name('z-page')  # find body wrapper
    print('Found wrapper')
except:
    print('Cannot find body wrapper, are you sure there is element with "z-page" class?')
    driver.quit()

try:
    unique_id = wrapper.get_attribute('id')[:-1]  # get wrapper's unique id
    print('Unique id is:', unique_id)
except:
    print('Cannot find unique id')
    driver.quit()


def addUniversitiesToList():
    rowUniversityCount = len(
        driver.find_elements_by_class_name('z-listcell-content')) # find universities content

    for i in range(rowUniversityCount): # for every university in table
        universityElement = driver.find_elements_by_class_name(
            "z-listcell-content")[i]  # find university row
        universityElement.click()  # click to university
        name = getElementText('4g-cap') # get university name
        print('Getting:', name.title()) # print university name
        appendUniversity() # append it.


addUniversitiesToList()
goNextPage()
driver.quit()

format_json = [ob.__dict__ for ob in university_list]
with io.open(output_file_name, 'w', encoding='utf8') as outfile:
    json.dump(format_json, outfile, sort_keys=True,
              indent=2, ensure_ascii=False)
