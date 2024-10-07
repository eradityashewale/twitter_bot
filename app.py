from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Correct path to the ChromeDriver executable
path = r'C:\Users\user\Downloads\edgedriver_win64\msedgedriver.exe'

# Create a Service object with the path to the ChromeDriver
service = Service(executable_path=path)

# Optional: Set up Chrome options (e.g., headless mode, disable notifications)
edge_options = webdriver.EdgeOptions()

# Initialize the Chrome WebDriver with the Service object and options
driver = webdriver.Edge(service=service, options=edge_options)

# Open Twitter
web = 'https://www.twitter.com'
driver.get(web)

# Wait until the login button is clickable and click it
try:
    close = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@class='css-175oi2r r-sdzlij r-1phboty r-rs99b7 r-lrvibr r-2yi16 r-1qi8awa r-3pj75a r-1loqt21 r-o7ynqc r-6416eg r-1ny4l3l']"))
    )
    close.click()
    login = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='/login']"))
    )
    login.click()
except Exception as e:
    print(f"Error occurred: {e}")

# Optional: Add some wait time to see the result
time.sleep(100)

# Close the browser
driver.quit()