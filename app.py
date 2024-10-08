from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from configparser import ConfigParser
import pandas as pd

# Load configuration
config = ConfigParser()
config.read('config.ini')
user_name = config["X"]['username']  # Use a different variable name for credentials
user_password = config["X"]['password']
email = config["X"]['email']

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
username_field = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@autocomplete='username']")))
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

# Go to the Explore page
search_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/explore']")))
search_button.click()

# Search for 'python'
search_text = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@role='combobox']")))
search_text.send_keys('python')

search_for = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, ".//span[contains(text(), 'Search for')]")))
search_for.click()

# Wait for the tweets to load
tweets = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//article[@role='article']")))

# Initialize lists for tweet data
user_data = []
text_data = []

# Iterate over each tweet element and extract the user and text
for tweet in tweets:
    try:
        user = tweet.find_element(By.XPATH, ".//span[contains(text(), '@')]").text
        text = tweet.find_element(By.XPATH, ".//div[@lang]").text
        user_data.append(user)
        text_data.append(text)
    except Exception as e:
        print("Error extracting tweet data:", e)

time.sleep(10)

# Close the browser
driver.quit()

# Save the tweets to a CSV file
df_tweets = pd.DataFrame({'user': user_data, 'text': text_data})
df_tweets.to_csv('tweets.csv', index=False)
print(df_tweets)
