from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import re
# import pandas as pd
import os
import sys
import json
import io

# set variables
driver_path = "./geckodriver.exe"  # browser driver path / firefox in this case
url = "https://eyoksis.yok.gov.tr/websitesiuygulamalari/harita/"  # launch yök url
sys.tracebacklimit = 0
universityList = []

# create a new firefox session
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options, executable_path=driver_path)
driver.implicitly_wait(1)
driver.get(url)

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


# get unique id's prefix
try:
    wrapper = driver.find_element_by_class_name('z-page')  # find body wrapper
    print('Found wrapper')
except (Exception, KeyboardInterrupt) as exc:
    print('Cannot find body wrapper, are you sure there is element with "z-page" class?')
    driver.quit()
    sys.exit(exc)

try:
    unique_id = wrapper.get_attribute('id')[:-1]  # get wrapper's unique id
    print('Unique id is:', unique_id)
except (Exception, KeyboardInterrupt) as exc:
    print('Cannot find unique id')
    driver.quit()
    sys.exit(exc)


def getElementText(afterPrefix):
    return driver.find_element_by_id(unique_id + afterPrefix).text


def setUniversity():
    name = getElementText('4g-cap')
    phone = getElementText('bg')
    fax = getElementText('jg')
    web = getElementText('rg')
    email = getElementText('zg')
    address = getElementText('6h')
    warden = getElementText('eh')

    universityList.append(University(
        name, phone, fax, web, email, address, warden))

    close_button = driver.find_element_by_class_name("z-window-close")
    close_button.click()


def clickNextButton():
    nextButton = driver.find_element_by_class_name('z-paging-next')
    nextButton.click()
    try:
        isNextButtonDisabled = nextButton.get_attribute('disabled')
        if isNextButtonDisabled == True:
            print('Checked every page')
    except:
        addUniversitiesToList()
        clickNextButton()


def addUniversitiesToList():
    rowUniversityCount = len(
        driver.find_elements_by_class_name('z-listcell-content'))

    for i in range(rowUniversityCount):
        universityElement = driver.find_elements_by_class_name(
            "z-listcell-content")[i]  # find university row
        universityElement.click()  # click to university
        name = getElementText('4g-cap')
        print('Getting:', name.title())
        setUniversity()


addUniversitiesToList()
clickNextButton()
driver.quit()

format_json = [ob.__dict__ for ob in universityList]
with io.open('SO_jsonout.json', 'w', encoding='utf8') as outfile:
    json.dump(format_json, outfile, sort_keys=True, indent=2, ensure_ascii=False)
