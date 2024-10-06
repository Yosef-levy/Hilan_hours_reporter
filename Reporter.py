import time
from selenium import webdriver
from selenium.webdriver.common.by import By

import Conf

URL = 'https://mobileye.net.hilan.co.il/Hilannetv2/ng/personal-file/home'
USERNAME_XPATH = '//*[@id="user_nm"]'
PASSWORD_XPATH = '//*[@id="password_nm"]'
LOG_BUTTON_XPATH = '//*[@id="mainViewPlaceholder"]/div/div/div[5]/button'
# REPORT_XPATH = '//h-app-component-layout//h-home-header//div[2]//div[1]/div/div[2]'
REPORT_XPATH = '//h-app-component-layout//h-display-attendance[1]//button[1]'
ENTRY_TIME_XPATH = '//*[@id="ctl00_mp_RG_Days_2408{}_{}_{}_cellOf_ManualEntry_EmployeeReports_row_0_0"]'
EXIT_TIME_XPATH = '//*[@id="ctl00_mp_RG_Days_2408{}_{}_{}_cellOf_ManualExit_EmployeeReports_row_0_0_ManualExit_EmployeeReports_row_0_0"]'
SUBMIT_BUTTON_XPATH = '//*[@id="ctl00_mp_RG_Days_2408{}_{}_{}_BtnsContainer"]/div[2]'


def report(username, password, start, end, location):
    try:
        driver = webdriver.Chrome()
        driver.get(URL)
        # Log in:
        buttons = driver.find_element(by=By.XPATH, value=USERNAME_XPATH)
        buttons.send_keys(username)
        if password:
            buttons = driver.find_element(by=By.XPATH, value=PASSWORD_XPATH)
            buttons.send_keys(password)
        buttons = driver.find_element(by=By.XPATH, value=LOG_BUTTON_XPATH)
        buttons.click()
        time.sleep(2)
        # Go to report system:
        try:
            buttons = driver.find_element(by=By.XPATH, value=REPORT_XPATH)
        except:
            time.sleep(3)
            buttons = driver.find_element(by=By.XPATH, value=REPORT_XPATH)
        buttons.click()
        time.sleep(2)
        # enter start/end times
        year = time.localtime(time.time()).tm_year
        month = f"{time.localtime(time.time()).tm_mon:02}"
        buttons = driver.find_element(by=By.XPATH, value=ENTRY_TIME_XPATH.format(username, year, month))
        buttons.click()
        input_field = buttons.find_element(by=By.TAG_NAME, value='input')
        input_field.send_keys('\b'*4 + start.replace(':', '') + end.replace(':', '') + '\t' + location)
        buttons = driver.find_element(by=By.XPATH, value=SUBMIT_BUTTON_XPATH.format(username, year, month))
        buttons.click()
        time.sleep(3)
        Conf.update_today_reported()
    except Exception as e:
        print(e)
        time.sleep(5)

