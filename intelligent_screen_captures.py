from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import os

# Ensure the data directory exists
os.makedirs('data', exist_ok=True)

# Credentials for login
username = "asdf"
password = "asdf"

# URLs to visit
urls = {
    '1st_floor_space_temps': 'https://10.200.200.26/hui/hui.html#app=graphics&view=STATUS&obj=/uidata/Custom%20Graphics/First_Floor/First_Floor.html&extra=/evox/equipment/generic/generic/6',
    'vav_1_12': 'https://10.200.200.26/hui/hui.html#app=graphics&view=STATUS&obj=/uidata/Custom%20Graphics/vav_stc_vcwf_Add_Reheat/vav_stc_vcwf_Add_Reheat.html&extra=/evox/equipment/scc/vav/4',
    'vav_1_1': 'https://10.200.200.26/hui/hui.html#app=graphics&view=STATUS&obj=/uidata/Custom%20Graphics/vav_stc_vcwf_Add_Reheat/vav_stc_vcwf_Add_Reheat.html&extra=/evox/equipment/scc/vav/7',
    'vav_1_13': 'https://10.200.200.26/hui/hui.html#app=graphics&view=STATUS&obj=/uidata/Custom%20Graphics/vav_stc_vcwf_Add_Reheat/vav_stc_vcwf_Add_Reheat.html&extra=/evox/equipment/scc/vav/5',
    'vav_1_5': 'https://10.200.200.26/hui/hui.html#app=graphics&view=STATUS&obj=/uidata/Custom%20Graphics/vav_stc_vcwf_Add_Reheat/vav_stc_vcwf_Add_Reheat.html&extra=/evox/equipment/scc/vav/11',
    'vav_1_8': 'https://10.200.200.26/hui/hui.html#app=graphics&view=STATUS&obj=/uidata/std/vav_stc_vcwf/vav_stc_vcwf.html&extra=/evox/equipment/scc/vav/40',
    '2nd_floor_space_temps': 'https://10.200.200.26/hui/hui.html#app=graphics&view=STATUS&obj=/uidata/Custom%20Graphics/Second_Floor/Second_Floor.html&extra=/evox/equipment/generic/generic/6',
    'vav_2_1': 'https://10.200.200.26/hui/hui.html#app=graphics&view=STATUS&obj=/uidata/std/vav_stc_vcwf/vav_stc_vcwf.html&extra=/evox/equipment/scc/vav/36',
    'vav_2_14': 'https://10.200.200.26/hui/hui.html#app=graphics&view=STATUS&obj=/uidata/Custom%20Graphics/vav_stc_vcwf_Add_Reheat/vav_stc_vcwf_Add_Reheat.html&extra=/evox/equipment/scc/vav/25',
    'vav_2_12': 'https://10.200.200.26/hui/hui.html#app=graphics&view=STATUS&obj=/uidata/std/vav_stc_vcwf/vav_stc_vcwf.html&extra=/evox/equipment/scc/vav/38',
    'vav_2_9': 'https://10.200.200.26/hui/hui.html#app=graphics&view=STATUS&obj=/uidata/Custom%20Graphics/vav_stc_vcwf_Add_Reheat/vav_stc_vcwf_Add_Reheat.html&extra=/evox/equipment/scc/vav/34',
    'vav_2_4': 'https://10.200.200.26/hui/hui.html#app=graphics&view=STATUS&obj=/uidata/Custom%20Graphics/vav_stc_vcwf_Add_Reheat/vav_stc_vcwf_Add_Reheat.html&extra=/evox/equipment/scc/vav/20',
    'rtu': 'https://10.200.200.26/hui/hui.html#app=graphics&view=STATUS&obj=/uidata/Custom%20Graphics/WECC_RL_060/WECC_RL_060.html&extra=/evox/equipment/dac/generic/2',
    'boiler': 'https://10.200.200.26/hui/hui.html#app=graphics&view=STATUS&obj=/uidata/Custom%20Graphics/Hot%20Water%20System/Hot%20Water%20System.html&extra=/evox/equipment/generic/generic/6'
}

# Initialize the WebDriver for Edge
service = Service('C:/Users/BBartling/Documents/edgedriver_win64/msedgedriver.exe')  # Update with the path to your WebDriver
options = webdriver.EdgeOptions()
options.add_argument('--ignore-certificate-errors')  # Ignore SSL certificate errors
driver = webdriver.Edge(service=service, options=options)

# Function to log in to the site
def login():
    driver.get('https://10.200.200.26/hui/index.html')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "userid")))
    
    # Locate the username and password fields and the login button
    username_field = driver.find_element(By.NAME, "userid")
    password_field = driver.find_element(By.NAME, "password")
    login_button = driver.find_element(By.ID, "logon")

    # Enter the username and password
    username_field.send_keys(username)
    password_field.send_keys(password)

    # Click the login button
    login_button.click()
    WebDriverWait(driver, 10).until(EC.url_contains("hui.html"))  # Adjust this as needed for a successful login

try:
    # Perform login
    login()
    
    # Set the browser to full screen
    driver.fullscreen_window()
    driver.execute_script("document.body.style.zoom='100%'")  # Adjust the zoom level as needed

    while True:
        for device_name, url in urls.items():
            print(f"Opening URL for {device_name}: {url}")
            driver.get(url)
            time.sleep(10)  # Wait for the page to load

            # Take a screenshot
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            screenshot_path = f"data/{device_name}_{timestamp}.png"
            driver.save_screenshot(screenshot_path)
            print(f"Screenshot saved: {screenshot_path}")

        print("Completed one loop. Waiting for 10 minutes before the next iteration.")
        time.sleep(600)  # Wait for 10 minutes before the next iteration
finally:
    driver.quit()
    print("WebDriver closed.")
