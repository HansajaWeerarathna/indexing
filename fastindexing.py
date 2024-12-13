import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# List of URLs (hardcoded)
urls = [
    "http://example1.com",
    "http://example2.com",
    "http://example3.com"
]

# Set up Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run browser in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
chrome_options.add_argument("--no-sandbox")  # Disable the sandbox for security reasons

# Specify the path to the chromedriver executable
chromedriver_path = '/usr/lib/chromium-browser/chromedriver'  # Adjust path if needed

# Create a Service object with the path to the driver
service = Service(executable_path=chromedriver_path)

# Set up the WebDriver (Chrome with options)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Function to wait until the page has fully loaded by checking the document's ready state
def wait_until_loaded(driver, max_wait_time=300):
    logger.info("Waiting for the page to finish loading...")
    WebDriverWait(driver, max_wait_time).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )
    logger.info("Page has finished loading.")

# Main function
def process_urls():
    for url in urls:
        logger.info(f"Processing URL: {url}")
        
        # Open the website
        driver.get("https://fastindex.wiki/")
        logger.info("Navigated to the website.")
        
        # Wait for the page to load
        wait_until_loaded(driver)
        
        # Find the input field and submit button by their XPath
        search_box = driver.find_element(By.XPATH, "/html/body/section[2]/div/form/div/input")  # URL input field
        submit_button = driver.find_element(By.XPATH, "/html/body/section[2]/div/form/button")  # Submit button
        
        # Enter the URL into the search box and submit it
        search_box.clear()  # Clear any pre-existing value
        search_box.send_keys(url)  # Enter the new URL
        logger.info(f"Entered URL: {url}")
        
        submit_button.click()  # Click the submit button
        logger.info("Clicked the Submit button.")
        
        # Wait for the page to load after submission
        wait_until_loaded(driver)
        
        # Refresh the page before going to the next URL
        driver.refresh()
        logger.info("Page refreshed after submission.")
        
        # Wait a little before moving on to the next URL
        time.sleep(5)  # Adjust the delay as needed
        logger.info("Waiting before processing the next URL...\n")

# Run the script once (this will be called by the cron job)
try:
    process_urls()
except Exception as e:
    logger.error(f"An error occurred: {e}")
finally:
    # Close the browser after processing all URLs
    logger.info("Closing the browser.")
    driver.quit()
