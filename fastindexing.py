import os
import subprocess
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# List of URLs (hardcoded)
urls = [
    "https://bestbusinesses.space/sitemap.xml",
    "https://bestbusinesses.space/random-sitemap.xml",
    "https://bestbusinesses.space/random-sitemap.xml", 
    'https://bestbusinesses.space/random-sitemap.xml', 
    'https://bestbusinesses.space/random-sitemap.xml', 
    'https://bestbusinesses.space/random-sitemap.xml', 
    "https://ustopbusiness.online/sitemap.xml",
    "https://ustopbusiness.online/random-sitemap.xml",
    "https://ustopbusiness.online/random-sitemap.xml", 
    'https://ustopbusiness.online/random-sitemap.xml', 
    'https://ustopbusiness.online/random-sitemap.xml', 
    'https://ustopbusiness.online/random-sitemap.xml', 
    'https://sitemap.ustopbusiness.online/sitemap.xml', 
    "https://americantopbusiness.site/sitemap.xml",
    "https://americantopbusiness.site/random-sitemap.xml",
    "https://americantopbusiness.site/random-sitemap.xml", 
    'https://americantopbusiness.site/random-sitemap.xml', 
    'https://americantopbusiness.site/random-sitemap.xml', 
    'https://americantopbusiness.site/random-sitemap.xml', 
    "https://americanbusinesses.space/sitemap.xml",
    "https://americanbusinesses.space/random-sitemap.xml",
    "https://americanbusinesses.space/random-sitemap.xml", 
    'https://americanbusinesses.space/random-sitemap.xml', 
    'https://americanbusinesses.space/random-sitemap.xml', 
    'https://americanbusinesses.space/random-sitemap.xml', 
    'https://sitemap.bestbusinesses.space/sitemap.xml', 
    'https://sitemap.americantopbusiness.site/sitemap.xml',
    'https://sitemap.americanbusinesses.space/sitemap.xml'
]

# Environment Variables for Configuration
chromedriver_path = os.getenv('CHROMEDRIVER_PATH', '/usr/lib/chromium-browser/chromedriver')
repo_directory = os.getenv('REPO_DIRECTORY', '/var/indexing')
log_file_path = os.getenv('LOG_FILE_PATH', '/var/indexing/fastindexing.log')

# Set up Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run browser in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
chrome_options.add_argument("--no-sandbox")  # Disable the sandbox for security reasons
chrome_options.add_argument("--no-proxy-server")  # Ensure no proxy is being used
chrome_options.add_argument("--proxy-server='direct://'")  # Bypass proxy settings

# Enable logging for ChromeDriver (for network issues)
caps = DesiredCapabilities.CHROME
caps['loggingPrefs'] = {'performance': 'ALL'}  # Enable network logs

# Create a Service object with the path to the driver
service = Service(executable_path=chromedriver_path)

# Function to prepend new logs to the beginning of the log file
def prepend_log_to_file(log_message):
    try:
        # Read the current log file content
        if os.path.exists(log_file_path):
            with open(log_file_path, 'r') as file:
                existing_logs = file.read()
        else:
            existing_logs = ''

        # Prepend the new log message to the existing logs
        full_log_content = log_message + '\n' + existing_logs
        
        # Write the full content back to the log file
        with open(log_file_path, 'w') as file:
            file.write(full_log_content)
    
    except Exception as e:
        print(f"Error while prepending to the log file: {e}")

# Function to initialize logging
def setup_logging():
    log_title = f"Processing started at: {time.strftime('%Y-%m-%d %H:%M:%S')}"
    prepend_log_to_file(log_title)  # Prepend the title to the log file

    # Set up logging configuration (this will log entries below the header)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # File handler for writing to log file
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    # Stream handler for real-time logging to console
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    # Add both handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger

# Function to push the log file to GitHub
def push_log_to_github():
    try:
        # Change to the directory of your Git repository
        os.chdir(repo_directory)  # Path to your GitHub repo

        # Add the log file to the git staging area
        subprocess.run(['git', 'add', log_file_path], check=True)

        # Commit the changes
        commit_message = f"Update log file: {time.strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)

        # Push the changes to GitHub
        subprocess.run(['git', 'push'], check=True)
        logger.info("Log file pushed to GitHub.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to push log file to GitHub: {e}")

# Function to wait until the page has fully loaded by checking the document's ready state
def wait_until_loaded(driver, max_wait_time=1200):  # Increased max wait time
    logger.info("Waiting for the page to finish loading...")
    try:
        WebDriverWait(driver, max_wait_time).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        logger.info("Page has finished loading.")

        # Wait for the page elements to be visible as well (e.g., form or buttons)
        WebDriverWait(driver, max_wait_time).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/section[2]/div/form/div/input'))
        )
        logger.info("Input field is visible and ready for interaction.")
    except TimeoutException:
        logger.error(f"Timeout occurred while waiting for the page to load within {max_wait_time} seconds.")

# Function to wait for overlays or modals to disappear
def wait_for_overlay_to_disappear(driver, overlay_xpath='//div[@class="overlay"]', max_wait_time=10):
    try:
        # Wait until the overlay disappears (you may need to adjust the XPath for your page)
        WebDriverWait(driver, max_wait_time).until(
            EC.invisibility_of_element_located((By.XPATH, overlay_xpath))
        )
        logger.info("Overlay disappeared.")
    except Exception as e:
        logger.warning(f"Overlay did not disappear in time: {e}")

# Function to click an element using JavaScript in case the normal click is blocked
def click_element_js(driver, element):
    driver.execute_script("arguments[0].click();", element)

# Function to click an element using ActionChains in case JavaScript clicking doesn't work
def click_element_with_actionchains(driver, element):
    try:
        actions = ActionChains(driver)
        actions.move_to_element(element).click().perform()  # Move to element and click
        logger.info("Clicked the Submit button using ActionChains.")
    except Exception as e:
        logger.error(f"Failed to click the element with ActionChains: {e}")

# Function to retry opening URL in case of timeout
def fetch_url_with_retry(driver, url, retries=5, delay=10):
    for attempt in range(retries):
        try:
            driver.get(url)
            logger.info(f"Successfully accessed URL: {url}")
            return True  # Success
        except TimeoutException:
            logger.error(f"Timeout while accessing {url} (Attempt {attempt + 1}/{retries})")
        except WebDriverException as e:
            logger.error(f"WebDriver exception while accessing {url}: {e}")
        except Exception as e:
            logger.error(f"General exception while accessing {url}: {e}")
        
        # Retry logic
        if attempt < retries - 1:
            logger.info(f"Retrying in {delay} seconds...")
            time.sleep(delay)
        else:
            logger.error(f"Failed to access {url} after {retries} attempts.")
            return False

# Main function
def process_urls():
    global driver  # Declare driver as global to access it in finally block

    # Initialize WebDriver with enhanced capabilities for network logging
    driver = webdriver.Chrome(service=service, options=chrome_options, desired_capabilities=caps)

    # Counter to track how many URLs have been processed
    url_counter = 0
    max_urls_before_restart = 5  # Restart the browser after processing 5 URLs
    try:
        for url in urls:
            url_counter += 1
            logger.info(f"Processing URL #{url_counter}: {url}")
            
            # Fetch URL with retry logic
            if fetch_url_with_retry(driver, url):
                wait_until_loaded(driver)

                # Additional actions you may want to do with the page
                # For example, filling out a form or interacting with elements
                try:
                    input_field = driver.find_element(By.XPATH, '/html/body/section[2]/div/form/div/input')
                    input_field.send_keys('Some data')
                    submit_button = driver.find_element(By.XPATH, '/html/body/section[2]/div/form/div/button')
                    submit_button.click()
                    logger.info(f"Form submitted on {url}")
                except NoSuchElementException:
                    logger.error(f"Form elements not found on {url}")
            
            # Check if it's time to restart WebDriver
            if url_counter >= max_urls_before_restart:
                logger.info(f"Restarting WebDriver after processing {url_counter} URLs.")
                driver.quit()  # Quit the current session
                driver = webdriver.Chrome(service=service, options=chrome_options, desired_capabilities=caps)  # Restart driver
                url_counter = 0  # Reset URL counter
            
            # Optional: wait between URL fetches
            time.sleep(5)  # Adjust as necessary
    except Exception as e:
        logger.error(f"Error processing URLs: {e}")
    finally:
        driver.quit()  # Make sure to quit the WebDriver at the end

# Run the script
if __name__ == "__main__":
    logger = setup_logging()
    process_urls()
    push_log_to_github()  # Optional, if you want to push the log to GitHub after processing
