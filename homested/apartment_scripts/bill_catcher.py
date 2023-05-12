import os

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def query_nwc(customer_code=None, premises_code=None):
    options = FirefoxOptions()
    options.add_argument("--headless")

    # change the exe path
    driver = webdriver.Firefox(options=options)
    try:
        driver.get('https://www.nwcjamaica.com/bill_query.php')

        driver.execute_script("var element = document.getElementById('popup').remove();")

        driver.execute_script("""
                       const elements = document.getElementsByClassName('modal-backdrop');
                    while(elements.length > 0){
                        elements[0].parentNode.removeChild(elements[0]);
                    }
                       """)

        driver.find_element(By.ID, 'txtCustomerCode').send_keys(customer_code)
        driver.find_element(By.ID, 'txtPremisesCode').send_keys(premises_code)

        driver.find_element(By.XPATH, '//button[@value="Find"]').click()

        sleep(1)

        div_element = driver.execute_script("""
        return document.querySelector('div.col-lg-4.col-md-4.col-sm-12.col-xs-12');
        """)

        # get the p elements containing the data you want to extract
        p_elements = div_element.find_elements(By.CSS_SELECTOR, 'div.row p.form-control-static')

        # create a dictionary to store the values
        values = {}

        # iterate through the p elements and extract the data you want
        for p_element in p_elements:
            label_text = p_element.find_element(By.XPATH, './preceding-sibling::p').text
            if label_text in ['Balance Overdue', 'Bill Balance', 'Due Date']:
                value_text = p_element.text.replace(',', '')
                if label_text == 'Balance Overdue':
                    values['overdue'] = value_text
                elif label_text == 'Bill Balance':
                    values['balance'] = value_text
                elif label_text == 'Due Date':
                    values['date'] = value_text

        # print the values
        print(values)
        return values
    except:
        print("Unable to execute JS")
