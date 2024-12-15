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
from selenium.common.exceptions import NoSuchElementException, TimeoutException

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
def wait_until_loaded(driver, max_wait_time=600):  # Increased wait time
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
def fetch_url_with_retry(driver, url, retries=3, delay=5):
    for attempt in range(retries):
        try:
            driver.get(url)
            return True  # Success
        except TimeoutException:
            logger.error(f"Timeout while accessing {url} (Attempt {attempt + 1}/{retries})")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                logger.error(f"Failed to access {url} after {retries} attempts.")
                return False
        except Exception as e:
            logger.error(f"Error accessing {url}: {e}")
            return False

# Main function
def process_urls():
    global driver  # Declare driver as global to access it in finally block
    driver = webdriver.Chrome(service=service, options=chrome_options)  # Initialize WebDriver

    # Counter to track how many URLs have been processed
    url_counter = 0
    max_urls_before_restart = 5  # Restart the browser after processing 5 URLs

    for url in urls:
        # If 5 URLs have been processed, restart the browser
        if url_counter >= max_urls_before_restart:
            logger.info("Restarting browser after processing 5 URLs.")
            driver.quit()  # Close the current browser session
            driver = webdriver.Chrome(service=service, options=chrome_options)  # Restart the browser
            url_counter = 0  # Reset the counter
        
        # Start a new run with a timestamp
        log_title = f"\n\nProcessing started at: {time.strftime('%Y-%m-%d %H:%M:%S')}"
        prepend_log_to_file(log_title)  # Prepend the header for each URL batch
        logger.info(log_title)  # Log it to the logger as well
        
        logger.info(f"Processing URL: {url}")
        
        # Open the website
        driver.get("https://fastindex.wiki/")
        logger.info("Navigated to the website.")
        
        # Wait for the page to load
        wait_until_loaded(driver)
        
        # Wait for any overlay or modal to disappear before proceeding
        wait_for_overlay_to_disappear(driver, overlay_xpath='//div[@class="overlay"]')  # Adjust XPath to your overlay
        
        try:
            # Find the input field and submit button by their XPath
            search_box = driver.find_element(By.XPATH, "/html/body/section[2]/div/form/div/input")  # URL input field
            submit_button = driver.find_element(By.XPATH, "/html/body/section[2]/div/form/button")  # Submit button
            
            # Wait for the input field and submit button to be interactable
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(search_box))
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(submit_button))

            # Enter the URL into the search box and submit it
            search_box.clear()  # Clear any pre-existing value
            search_box.send_keys(url)  # Enter the new URL
            logger.info(f"Entered URL: {url}")
            
            # Scroll the submit button into view (if necessary)
            driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
            
            # Wait for animations to complete (if necessary)
            time.sleep(1)  # Adding a small delay to allow animations to finish
            
            # Try clicking using JavaScript if regular click is blocked
            click_element_js(driver, submit_button)
            logger.info("Clicked the Submit button.")
            
            # Wait for the page to load after submission
            wait_until_loaded(driver)
            
        except (NoSuchElementException, TimeoutException) as e:
            logger.error(f"An error occurred while processing the URL {url}: {e}")
        
        # Refresh the page before going to the next URL
        driver.refresh()
        logger.info("Page refreshed after submission.")
        
        # Wait a little before moving on to the next URL
        time.sleep(5)  # Adjust the delay as needed
        logger.info("Waiting before processing the next URL...\n")
        
        # Increment the URL counter
        url_counter += 1
    
    # After processing all URLs, push the log to GitHub
    push_log_to_github()


# Run the script once (this will be called by the cron job)
try:
    logger = setup_logging()  # Set up logging with the header prepended
    process_urls()
except Exception as e:
    logger.error(f"An error occurred: {e}")
finally:
    # Close the browser after processing all URLs
    logger.info("Closing the browser.")
    driver.quit()  # Now driver is defined
