from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from configparser import ConfigParser
import pandas as pd
from datetime import datetime, timedelta

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
edge_options.add_argument('--no-proxy-server')

# Initialize the Edge WebDriver with the Service object and options
# driver = webdriver.Edge(service=service, options=edge_options)
driver = webdriver.Chrome()

# Open Twitter
web = 'https://www.twitter.com'
driver.get(web)

# Wait for the close button and click it if it appears (e.g., cookie consent)
try:
    close_button = WebDriverWait(driver, 30).until(
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
search_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/explore']")))
search_button.click()

# Search for 'python'
search_text = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//input[@role='combobox']")))
search_text.send_keys('$eth')

search_for = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, ".//span[contains(text(), 'Search for')]")))
search_for.click()

# Wait for the tweets to load
# tweets = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//article[@role='article']")))

# Initialize lists for tweet data


time_limit = datetime.now() - timedelta(hours=12)
driver.implicitly_wait(10)  # Adjust the wait time as needed
user_data = []
text_data = []
comments_no_data = []
reposts_data = []
likes_data = []
views_data = []
image_urls = []
tweet_datetime = []

scrolling = True
while scrolling:
    try:
        # Wait until tweets load
        tweets = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.XPATH, "//article[@role='article']"))
        )
        
        print(f"Found {len(tweets)} tweets.")  # Log the number of tweets found
        
        for tweet in tweets:
            try:
                # Extract user handle
                user = tweet.find_element(By.XPATH, ".//span[contains(text(), '@')]").text
                print(f"User: {user}")  # Log user handle
                
                # Extract tweet text
                text = tweet.find_element(By.XPATH, ".//div[@lang]").text
                print(f"Text: {text}")  # Log tweet text
                
                # Extract comment count
                comments_no = tweet.find_element(By.XPATH, "//button[@data-testid='reply']//span[@data-testid='app-text-transition-container']//span").text
                print(f"Comments: {comments_no}")  # Log comment count
                
                # Extract repost count
                reposts = tweet.find_element(By.XPATH, "//button[@data-testid='retweet']//span[@data-testid='app-text-transition-container']//span").text
                print(f"Reposts: {reposts}")  # Log repost count
                
                # Extract like count
                likes = tweet.find_element(By.XPATH, "//button[@data-testid='like']//span[@data-testid='app-text-transition-container']//span").text
                print(f"Likes: {likes}")  # Log like count
                
                # Extract views count
                views = tweet.find_element(By.XPATH, "//a[contains(@aria-label, 'views')]//span[@data-testid='app-text-transition-container']//span").text
                print(f"Views: {views}")  # Log views count
                
                # Extract profile image URL
                image_url = tweet.find_element(By.XPATH, "//img[contains(@src, 'profile_images') or contains(@alt, 'Profile picture')]").getAttribute("src")
                print(f"Image URL: {image_url}")  # Log image URL
                
                # Extract tweet timestamp
                timestamp_element = tweet.find_element(By.XPATH, ".//time")
                tweet_time = timestamp_element.get_attribute("datetime")
                tweet_datetime_value = datetime.fromisoformat(tweet_time[:-1])  # Convert to datetime
                
                # Check if the tweet is older than 12 hours
                if tweet_datetime_value < time_limit:
                    scrolling = False
                    break
                
                # Append extracted data to lists
                user_data.append(user)
                text_data.append(text)
                comments_no_data.append(comments_no)
                reposts_data.append(reposts)
                likes_data.append(likes)
                views_data.append(views)
                image_urls.append(image_url)
                tweet_datetime.append(tweet_datetime_value)

                print("Data appended successfully")  # Log successful data append

            except Exception as e:
                print(f"Error extracting tweet data: {e}")
                continue  # Continue with the next tweet

        # Scroll down to load more tweets
        if scrolling:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Adjust sleep time as needed

    except Exception as e:
        print(f"Error fetching tweets: {e}")
        scrolling = False

# Check if data is correctly appended
print(f"user_data length: {len(user_data)}, text_data length: {len(text_data)}")
print(f"comments_no_data length: {len(comments_no_data)}, reposts_data length: {len(reposts_data)}")
print(f"likes_data length: {len(likes_data)}, views_data length: {len(views_data)}")

# Create DataFrame and save to CSV
if len(user_data) == len(text_data) == len(comments_no_data) == len(reposts_data) == len(likes_data) == len(views_data) == len(image_urls) == len(tweet_datetime):
    df_tweets = pd.DataFrame({
        'user': user_data,
        'text': text_data,
        'comments': comments_no_data,
        'reposts': reposts_data,
        'likes': likes_data,
        'views': views_data,
        'profile_image_url': image_urls,
        'tweet_datetime': tweet_datetime
    })
    
    df_tweets.to_csv('tweets.csv', index=False)
    print("Data saved to CSV successfully")
else:
    print("List lengths are not matching! Dataframe creation aborted.")