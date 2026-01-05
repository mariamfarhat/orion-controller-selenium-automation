import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
import time
import os
from selenium.common.exceptions import NoSuchElementException

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(BASE_DIR, "data", "test_snmp.xlsx")

#Check if data is being read from excel
df = pd.read_excel(file_path)
print(df)

#for each row read the following value
for row in df.itertuples(index=False):
    host = row.host
    port = row.port
    username = row.username
    password = row.password

    url = f"http://{host}:{port}/controller/login"
#Print the url to check the extracted values
    print("Opening:", url)
#Connect to URL
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 15)
driver = webdriver.Chrome()
driver.get(url)

time.sleep(2)  # Wait for the page to load

in_username = driver.find_element(By.NAME, "inputElement_un")
in_password = driver.find_element(By.NAME, "inputElement_pw")

in_username.send_keys(username)
in_password.send_keys(password)

#password.send_keys(Keys.RETURN)
driver.find_element(By.NAME, "formButton_submit").click()
time.sleep(10)  # Wait for login to complete 

url_time=f"http://{host}:{port}/controller/configuration/system/timedate"
driver.get(url_time)
time.sleep(15)
try:
    # Try to find input first (editable)
    field = driver.find_element(By.NAME, "value_10a0_0052_0000")
    current_value = field.get_attribute("value")
    print("Editable input found, current value:", current_value)
    field.clear()
    value_to_set = "192.168.1.1"
    field.send_keys(value_to_set)
    field.send_keys("\t")  # trigger JS
    print("Value updated to:", value_to_set)
    driver.find_element(By.NAME, "accept").click()
    driver.find_element(By.NAME, "reload").click()
    time.sleep(5)


except NoSuchElementException:
    # Fallback: find div (read-only)
    div_field = driver.find_element(By.ID, "measurement_10a0_0052_0000")
    current_value = div_field.text
    print("Read-only div found, value:", current_value)

time.sleep(10)