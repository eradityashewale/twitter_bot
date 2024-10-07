from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
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
web = 'https://twitter.com/'
driver.get(web)

# Find and click the login button
login = driver.find_element(By.XPATH, "//a[@href='/login']")
login.click()

# Sleep for 2 seconds to allow time for the next page to load
time.sleep(2)
