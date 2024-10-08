from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from configparser import ConfigParser

# Load configuration
config = ConfigParser()
config.read('config.ini')
user_name = config["X"]['username']  # Use a different variable name for credentials
user_password = config["X"]['password']

# Correct path to the EdgeDriver executable
path = r'C:\Users\user\Downloads\edgedriver_win64\msedgedriver.exe'

# Create a Service object with the path to the EdgeDriver
service = Service(executable_path=path)

# Set up Edge options (e.g., headless mode, disable notifications)
edge_options = webdriver.EdgeOptions()

# Initialize the Edge WebDriver with the Service object and options
driver = webdriver.Edge(service=service, options=edge_options)

# Open Twitter
web = 'https://www.twitter.com'
driver.get(web)

# Wait for the close button and click it if it appears (e.g., cookie consent)
try:
    close_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@class='css-175oi2r r-sdzlij r-1phboty r-rs99b7 r-lrvibr r-2yi16 r-1qi8awa r-3pj75a r-1loqt21 r-o7ynqc r-6416eg r-1ny4l3l']"))
    )
    close_button.click()
except Exception as e:
    print("No close button found or an error occurred:", e)

# Wait for the login button and click it
login = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/login']")))
login.click()

# Enter the username
username_field = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//input[@autocomplete='username']")))
username_field.send_keys(user_name)  # Use the variable holding the actual username from config

# Click 'Next' button
next_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']")))
next_button.click()

# Wait for the password field to be clickable and enter the password
password_field = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@autocomplete='current-password']")))
password_field.send_keys(user_password)  # Use the variable holding the actual password from config

# Click the 'Log In' button after entering the password
login_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Log in']")))
login_button.click()

# Optional: Add a wait to see the result before closing the browser
time.sleep(10)

# Close the browser
# driver.quit()
