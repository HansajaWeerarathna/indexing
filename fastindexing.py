import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
<<<<<<< HEAD
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException
=======
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import requests  # Ensure requests is imported
>>>>>>> a1e041d469ca2eafdae6abbfb889e635ccf5ae20

# List of URLs to process
urls = [
    "https://americantopbusiness.site/sitemap.xml",
    "https://americantopbusiness.site/random-sitemap.xml",
<<<<<<< HEAD
    "https://americantopbusiness.site/random-sitemap.xml", 
    'https://americantopbusiness.site/random-sitemap.xml', 
    'https://americantopbusiness.site/random-sitemap.xml', 
    'https://americantopbusiness.site/random-sitemap.xml', 
=======
    "https://americantopbusiness.site/random-sitemap.xml",
    "https://americantopbusiness.site/random-sitemap.xml", 
    "https://americantopbusiness.site/random-sitemap.xml", 
    "https://americantopbusiness.site/random-sitemap.xml", 
>>>>>>> a1e041d469ca2eafdae6abbfb889e635ccf5ae20
    "https://bestbusinesses.space/sitemap.xml",
    "https://bestbusinesses.space/random-sitemap.xml",
    "https://bestbusinesses.space/random-sitemap.xml", 
    "https://bestbusinesses.space/random-sitemap.xml", 
    "https://bestbusinesses.space/random-sitemap.xml", 
    "https://bestbusinesses.space/random-sitemap.xml", 
    "https://ustopbusiness.online/sitemap.xml",
    "https://ustopbusiness.online/random-sitemap.xml",
    "https://ustopbusiness.online/random-sitemap.xml", 
<<<<<<< HEAD
    'https://ustopbusiness.online/random-sitemap.xml', 
    'https://ustopbusiness.online/random-sitemap.xml', 
    'https://ustopbusiness.online/random-sitemap.xml', 
    "https://americanbusinesses.space/sitemap.xml",
    "https://americanbusinesses.space/random-sitemap.xml",
    "https://americanbusinesses.space/random-sitemap.xml", 
    'https://americanbusinesses.space/random-sitemap.xml', 
    'https://americanbusinesses.space/random-sitemap.xml', 
    'https://americanbusinesses.space/random-sitemap.xml', 
    'https://sitemap.bestbusinesses.space/sitemap.xml', 
    'https://sitemap.americantopbusiness.site/sitemap.xml',
    'https://sitemap.americanbusinesses.space/sitemap.xml', 
    'https://sitemap.ustopbusiness.online/sitemap.xml', 
=======
    "https://ustopbusiness.online/random-sitemap.xml", 
    "https://ustopbusiness.online/random-sitemap.xml", 
    "https://ustopbusiness.online/random-sitemap.xml", 
    "https://sitemap.bestbusinesses.space/sitemap.xml", 
    "https://sitemap.americantopbusiness.site/sitemap.xml",
    "https://sitemap.americanbusinesses.space/sitemap.xml", 
    "https://sitemap.ustopbusiness.online/sitemap.xml", 
    "https://americanbusinesses.space/sitemap.xml",
    "https://americanbusinesses.space/random-sitemap.xml",
    "https://americanbusinesses.space/random-sitemap.xml", 
    "https://americanbusinesses.space/random-sitemap.xml", 
    "https://americanbusinesses.space/random-sitemap.xml", 
    "https://americanbusinesses.space/random-sitemap.xml",
>>>>>>> a1e041d469ca2eafdae6abbfb889e635ccf5ae20
]

# urls = [
#     "https://newsapi.org/sitemap.xml", 
#     "https://newsapi.org/sitemap.xml", 
#     "https://newsapi.org/sitemap.xml"
#     ]

# Path to the chromedriver executable (adjust this for your system)
chromedriver_path = 'C:/Users/Acer/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe'  # Adjust to your chromedriver path

# Set up Chrome options without headless mode
chrome_options = Options()
# Removed headless mode
chrome_options.add_argument("--headless")  # This line has been removed
chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
<<<<<<< HEAD
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
=======
chrome_options.add_argument("--no-sandbox")  # Disable sandbox for security reasons
>>>>>>> a1e041d469ca2eafdae6abbfb889e635ccf5ae20

# Function to initialize logging
def setup_logging():
    log_file_path = 'fastindexing.log'  # Set path for log file
    log_title = f"Processing started at: {time.strftime('%Y-%m-%d %H:%M:%S')}"
    
    # Set up logging configuration
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

    logger.info(log_title)  # Log the start time
    return logger

<<<<<<< HEAD
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
=======
# Function to wait until the page has fully loaded
def wait_until_loaded(driver, max_wait_time=600):
>>>>>>> a1e041d469ca2eafdae6abbfb889e635ccf5ae20
    logger.info("Waiting for the page to finish loading...")
    try:
        # Wait until the document is fully loaded
        WebDriverWait(driver, max_wait_time).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

        # Additional check for a key element that signifies the page is ready (e.g., form or button visibility)
        WebDriverWait(driver, max_wait_time).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/section[2]/div/form/button"))
        )

        logger.info("Page has finished loading.")
    except TimeoutException:
        logger.error(f"Timeout occurred while waiting for the page to load.")

<<<<<<< HEAD
# Function to ensure element is clickable by waiting for visibility and clickability
def wait_for_clickable_element(driver, element, max_wait_time=30):
    for attempt in range(3):  # Retry up to 3 times
        try:
            WebDriverWait(driver, max_wait_time).until(
                EC.visibility_of(element)  # Ensure element is visible
            )
            WebDriverWait(driver, max_wait_time).until(
                EC.element_to_be_clickable(element)  # Ensure element is clickable
            )
            logger.info(f"Element is visible and clickable.")
            return True
        except TimeoutException:
            logger.error(f"Element not clickable within {max_wait_time} seconds. Retrying...")
            time.sleep(1)  # Wait a moment before retrying
            # Re-locate the element here if needed
    return False

# Function to click an element using JavaScript in case the normal click is blocked
def click_element_js(driver, element):
    try:
        # Use JavaScript to click the element
        driver.execute_script("arguments[0].click();", element)
        logger.info("Clicked the element using JavaScript.")
    except Exception as e:
        logger.error(f"Failed to click the element using JavaScript: {e}")

# Function to submit the form with retries
def submit_form_with_retry(driver, search_box, submit_button, url, retries=3, delay=10):
    for attempt in range(retries):
        try:
            # Clear and fill out the form
            search_box.clear()
            search_box.send_keys(url)
            logger.info(f"Entered URL: {url}")

            # Scroll the submit button into view
            driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)

            # Ensure submit button is clickable
            if wait_for_clickable_element(driver, submit_button):
                # Click the submit button using normal click or JS fallback
                try:
                    submit_button.click()
                    logger.info("Clicked the Submit button.")
                except Exception as e:
                    logger.warning(f"Normal click failed, trying JavaScript: {e}")
                    click_element_js(driver, submit_button)

                # Wait for the page to load after form submission
                wait_until_loaded(driver)
                return True  # Success

        except (NoSuchElementException, TimeoutException) as e:
            logger.error(f"Attempt {attempt + 1}: Failed to submit the form. Error: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                logger.error(f"Failed to submit the form after {retries} attempts.")
                return False

# Function to process URLs in batches
def process_batch(driver, urls_batch):
    global logger
    for url in urls_batch:
        logger.info(f"Processing URL: {url}")

        # Open the website
        driver.get("https://fastindex.wiki/")  # Visit the page to process the URLs
        logger.info("Navigated to the website.")

        # Wait for the page to load
        wait_until_loaded(driver)

        try:
            # Find the input field and submit button by their XPath
            search_box = driver.find_element(By.XPATH, "/html/body/section[2]/div/form/div/input")  # URL input field
            submit_button = driver.find_element(By.XPATH, "/html/body/section[2]/div/form/button")  # Submit button

            # Wait for the input field and submit button to be interactable
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(search_box))
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(submit_button))

            # Submit the form with retries
            if not submit_form_with_retry(driver, search_box, submit_button, url):
                logger.error(f"Failed to submit URL: {url} after retries.")
                continue

        except (NoSuchElementException, TimeoutException) as e:
            logger.error(f"An error occurred while processing the URL {url}: {e}")

        # Refresh the page before going to the next URL
        driver.refresh()
        logger.info("Page refreshed after submission.")

        # Wait a little before moving on to the next URL
        time.sleep(5)  # Adjust the delay as needed
        logger.info("Waiting before processing the next URL...\n")

# Main function to process URLs in batches and restart the browser as needed
def process_urls():
    global driver  # Declare driver as global to access it in finally block
    driver = webdriver.Chrome(service=service, options=chrome_options)  # Initialize WebDriver

    # Split the URLs into batches of 5
    batch_size = 5
    url_batches = [urls[i:i + batch_size] for i in range(0, len(urls), batch_size)]

    # Process each batch
    for batch_num, batch in enumerate(url_batches, 1):
        logger.info(f"\nProcessing batch {batch_num} of {len(url_batches)}...")
        process_batch(driver, batch)

        # Close the browser and wait 1 minute before starting the next batch
        driver.quit()
        logger.info(f"Batch {batch_num} completed. Closing the browser and waiting for 1 minute before the next batch.")
        time.sleep(60)  # Wait for 1 minute before the next batch

        # Reinitialize the browser for the next batch
        driver = webdriver.Chrome(service=service, options=chrome_options)

    # After processing all batches, push the log to GitHub
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
=======
# Function to process URLs one by one
def process_urls():
    global driver  # Declare driver as global to access it in finally block
    
    # Set up the Chrome WebDriver without headless mode
    driver = webdriver.Chrome(service=Service(executable_path=chromedriver_path), options=chrome_options)  # Initialize WebDriver
    
    # Process each URL
    for url in urls:
        try:
            logger.info(f"Processing URL: {url}")

            # Open the website
            driver.get("https://fastindex.wiki/")  # Visit the page to process the URLs
            logger.info("Navigated to the website.")

            # Wait for the page to load
            wait_until_loaded(driver)

            # Find the input field and submit button by their XPath
            search_box = driver.find_element(By.XPATH, "/html/body/section[2]/div/form/div/input")  # URL input field
            submit_button = driver.find_element(By.XPATH, "/html/body/section[2]/div/form/button")  # Submit button

            # Clear and fill out the form
            search_box.clear()
            search_box.send_keys(url)
            logger.info(f"Entered URL: {url}")

            # Click the submit button
            submit_button.click()
            logger.info("Clicked the Submit button.")

            # Wait for the page to load after form submission
            wait_until_loaded(driver)

            # Log completion for the URL
            logger.info(f"Finished processing URL: {url}")

        except Exception as e:
            logger.error(f"An error occurred while processing the URL {url}: {e}")

    # After processing all URLs, close the browser
    logger.info("Processing completed. Closing the browser.")
    driver.quit()

# Main script execution
if __name__ == "__main__":
    logger = setup_logging()
    process_urls()
>>>>>>> a1e041d469ca2eafdae6abbfb889e635ccf5ae20
