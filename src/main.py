import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def login_with_selenium(driver, url, username, password):
    wait = WebDriverWait(driver, 15)
    try:
        driver.get(url)
        # Wait for username field to be present
        in_username = wait.until(EC.presence_of_element_located((By.NAME, "inputElement_un")))
        in_password = driver.find_element(By.NAME, "inputElement_pw")
        in_username.send_keys(username)
        in_password.send_keys(password)
        driver.find_element(By.NAME, "formButton_submit").click()
        print(f"Login successful! Proceeding to time & Date Configuration.")
        return True, "Login successful"

    except TimeoutException:
        return False, "Login timeout: elements not found within 10 seconds"
    except Exception as e:
        print(f"Login Failed or element not found:", e)
        return False, str(e)

def change_ntp_server(driver, url_time):
    wait = WebDriverWait(driver, 15)
    try:
        driver.get(url_time)
        # Wait for the NTP field to be present
        field = wait.until(EC.presence_of_element_located((By.NAME, "value_10a0_0052_0000")))
        current_value = field.get_attribute("value")
        print("Editable input found, current value:", current_value)
        field.clear()
        value_to_set = "192.168.1.1"
        field.send_keys(value_to_set)
        field.send_keys("\t")  # trigger JS
        print("Value updated to:", value_to_set)
        accept_button = wait.until(EC.element_to_be_clickable((By.NAME, "accept")))
        accept_button.click()
        reload_button = wait.until(EC.element_to_be_clickable((By.NAME, "reload")))
        reload_button.click()
        # Wait a bit for reload
        time.sleep(2)
        return True, "NTP server changed successfully"

    except TimeoutException:
        return False, "Timeout: NTP elements not found or not clickable within 10 seconds"
    except NoSuchElementException:
        # Fallback: find div (read-only)
        try:
            div_field = wait.until(EC.presence_of_element_located((By.ID, "measurement_10a0_0052_0000")))
            current_value = div_field.text
            print("Read-only div found, value:", current_value)
            return False, "NTP server is read-only"
        except TimeoutException:
            return False, "Timeout: NTP read-only field not found"
        except Exception as e:
            return False, f"Error accessing NTP field: {str(e)}"
    except Exception as e:
        return False, f"Error changing NTP server: {str(e)}"

def main():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(BASE_DIR, "data", "test_snmp.xlsx")
    output_path = os.path.join(BASE_DIR, "data", "results.xlsx")

    # Check if data is being read from excel
    df = pd.read_excel(file_path)
    print(df)

    results = []

    for row in df.itertuples(index=False):
        row_dict = row._asdict()
        url = f"http://{row.host}:{row.port}/controller/login"
        print("Opening:", url)

        # Create driver for each row
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        try:
            # Call login function
            login_success, login_reason = login_with_selenium(driver, url, row.username, row.password)
            if not login_success:
                row_dict['status'] = 'Failed'
                row_dict['reason'] = f"Login failed: {login_reason}"
                print(f"Login failed for {row.host}:{row.port}")
            else:
                url_time = f"http://{row.host}:{row.port}/controller/configuration/system/timedate"
                print("Opening:", url_time)
                ntp_success, ntp_reason = change_ntp_server(driver, url_time)
                if ntp_success:
                    row_dict['status'] = 'Successful'
                    row_dict['reason'] = ntp_reason
                    print(f"NTP change successful for {row.host}:{row.port}")
                else:
                    row_dict['status'] = 'Failed'
                    row_dict['reason'] = f"NTP change failed: {ntp_reason}"
                    print(f"NTP change failed for {row.host}:{row.port}")
        except Exception as e:
            row_dict['status'] = 'Failed'
            row_dict['reason'] = f"Unexpected error: {str(e)}"
            print(f"Unexpected error for {row.host}:{row.port}: {e}")
        finally:
            driver.quit()

        results.append(row_dict)

    # Write results to Excel
    results_df = pd.DataFrame(results)
    results_df.to_excel(output_path, index=False)
    print(f"Results written to {output_path}")
        
if __name__ == "__main__":
    main()
