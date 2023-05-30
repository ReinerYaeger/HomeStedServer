import json
import os
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions


class web_scraper:

    def __init__(self):
        pass

    def query_jps(self):
        jps_bill = 0
        return jps_bill

    def query_internet(self):
        return 0

    @staticmethod
    def query_nwc(customer_code=None, premises_code=None):
        script_dir = os.path.dirname(os.path.abspath(__file__))

        file_name = 'current_water_bill.txt'
        file_path = os.path.join(script_dir, file_name)

        modification_time = os.path.getmtime(file_path)
        modification_date = datetime.fromtimestamp(modification_time)

        time_difference = datetime.now() - modification_date
        two_weeks = timedelta(days=30)
        if not os.path.exists(file_path):
                open(file_path, 'w')

        # if the current_water_bill has been modified within 30 days, I will read from the file if not perform the webscrape

        if two_weeks > timedelta(hour=1) > time_difference :
            with open(file_path, 'r') as f:
                bill_dict = json.load(f)
            return bill_dict

        else:

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

                p_elements = div_element.find_elements(By.CSS_SELECTOR, 'div.row p.form-control-static')

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

                with open(file_path, "w") as file:
                    file.write(json.dumps(values))

                print(values)
                return values
            except:
                print("Unable to execute JS")
