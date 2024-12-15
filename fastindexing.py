import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# List of URLs to process
urls = [
    "https://americantopbusiness.site/sitemap.xml",
    "https://americantopbusiness.site/random-sitemap.xml",
    "https://americantopbusiness.site/random-sitemap.xml",
    "https://americantopbusiness.site/random-sitemap.xml", 
    "https://americantopbusiness.site/random-sitemap.xml", 
    "https://americantopbusiness.site/random-sitemap.xml", 
    "https://bestbusinesses.space/sitemap.xml",
    "https://bestbusinesses.space/random-sitemap.xml",
    "https://bestbusinesses.space/random-sitemap.xml", 
    "https://bestbusinesses.space/random-sitemap.xml", 
    "https://bestbusinesses.space/random-sitemap.xml", 
    "https://bestbusinesses.space/random-sitemap.xml", 
    "https://ustopbusiness.online/sitemap.xml",
    "https://ustopbusiness.online/random-sitemap.xml",
    "https://ustopbusiness.online/random-sitemap.xml", 
    "https://ustopbusiness.online/random-sitemap.xml", 
    "https://ustopbusiness.online/random-sitemap.xml", 
    "https://ustopbusiness.online/random-sitemap.xml", 
    "https://americanbusinesses.space/sitemap.xml",
    "https://americanbusinesses.space/random-sitemap.xml",
    "https://americanbusinesses.space/random-sitemap.xml", 
    "https://americanbusinesses.space/random-sitemap.xml", 
    "https://americanbusinesses.space/random-sitemap.xml", 
    "https://americanbusinesses.space/random-sitemap.xml", 
    "https://sitemap.bestbusinesses.space/sitemap.xml", 
    "https://sitemap.americantopbusiness.site/sitemap.xml",
    "https://sitemap.americanbusinesses.space/sitemap.xml", 
    "https://sitemap.ustopbusiness.online/sitemap.xml"
]

# Path to the chromedriver executable (adjust this for your system)
chromedriver_path = 'C:/Users/Acer/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe'  # Adjust to your chromedriver path

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
chrome_options.add_argument("--no-sandbox")  # Disable sandbox for security reasons

# Create a Service object with the path to the driver
service = Service(executable_path=chromedriver_path)

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

# Function to wait until the page has fully loaded
def wait_until_loaded(driver, max_wait_time=600):
    logger.info("Waiting for the page to finish loading...")
    try:
        WebDriverWait(driver, max_wait_time).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        logger.info("Page has finished loading.")
    except TimeoutException:
        logger.error(f"Timeout occurred while waiting for the page to load within {max_wait_time} seconds.")

# Function to ensure element is clickable
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
    return False

# Function to click an element using JavaScript if normal click fails
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

# Function to process URLs one by one
def process_urls():
    global driver  # Declare driver as global to access it in finally block
    driver = webdriver.Chrome(service=service, options=chrome_options)  # Initialize WebDriver

    # Process each URL
    for url in urls:
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

    # After processing all URLs, close the browser
    logger.info("Processing completed. Closing the browser.")
    driver.quit()

# Run the script
try:
    logger = setup_logging()  # Set up logging
    process_urls()
except Exception as e:
    logger.error(f"An error occurred: {e}")
finally:
    # Close the browser after processing all URLs
    logger.info("Closing the browser.")
    if 'driver' in locals():  # Check if driver is defined
        driver.quit()  # Now driver is defined
