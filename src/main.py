from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

import os
import pandas as pd
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = os.getenv('LOGIN_URL', 'default-url')
USERNAME = os.getenv('USERNAME', '')
PASSWORD = os.getenv('PASSWORD', '')

app = Flask(__name__)

@app.route('/process_msisdns', methods=['POST'])
def process_msisdns():
    msisdns = request.json['msisdns']
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--ignore-ssl-errors=yes")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-urlfetcher-cert-requests')
    options.accept_insecure_certs = True

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(URL)

    login = driver.find_element(By.NAME, 'login')
    password = driver.find_element(By.NAME, 'password')
    connect_btn = driver.find_element(By.XPATH, '//*[@id="login-form"]/fieldset/div[3]/input')
    login.clear()
    login.send_keys(USERNAME)
    password.clear()
    password.send_keys(PASSWORD)
    connect_btn.click()

    dm_center_btn = driver.find_element(By.XPATH, '//*[@id="module-list"]/div[1]/a')
    dm_center_btn.click()

    msisdn_dict = {'msisdn': [], 'imei_count': []}
    for msisdn in msisdns:
        msisdn = '+' + msisdn
        msisdn_box = driver.find_element(By.NAME, 'MSISDN')
        msisdn_box.send_keys(msisdn)
        search_btn = driver.find_element(By.NAME, 'filter')
        search_btn.click()
        msisdn_box = driver.find_element(By.NAME, 'MSISDN')
        msisdn_box.clear()

        msisdn_results = driver.find_elements(By.XPATH, '//*[@id="subscribers"]/tbody/tr')
        for i in range(len(msisdn_results)):
            imei_value = driver.find_element(By.XPATH, '//*[@id="subscribers"]/tbody/tr/td[3]').text
            imei_box = driver.find_element(By.NAME, 'IMEI')
            imei_box.send_keys(imei_value)
            search_btn = driver.find_element(By.NAME, 'filter')
            search_btn.click()
            imei_results = driver.find_elements(By.XPATH, '//*[@id="subscribers"]/tbody/tr')
            try:
                num_pages = int((driver.find_element(By.XPATH, '//*[@id="subscribers"]/thead/tr[1]/td/span[1]').text)[-2:])
                page_box = driver.find_element(By.XPATH, '//*[@id="subscribers"]/thead/tr[1]/td/div[1]/form/input[1]')
                page_box.send_keys(num_pages)
                go_btn = driver.find_element(By.XPATH, '//*[@id="subscribers"]/thead/tr[1]/td/div[1]/form/input[2]')
                go_btn.click()
                num_pages = 25 * (num_pages - 1) + len(driver.find_elements(By.XPATH, '//*[@id="subscribers"]/tbody/tr'))
            except Exception as e:
                num_pages = len(imei_results)

            imei_box = driver.find_element(By.NAME, 'IMEI')
            imei_box.clear()

        msisdn_dict['msisdn'].append(msisdn)
        msisdn_dict['imei_count'].append(num_pages)

    driver.quit()

    return jsonify(msisdn_dict)

if __name__ == '__main__':
    app.run()