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
import requests  # Ensure requests is imported

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
chrome_options.add_argument("--no-sandbox")  # Disable sandbox for security reasons

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
