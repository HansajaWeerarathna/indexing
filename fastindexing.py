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

# List of URLs (hardcoded)
# urls = [
#     "https://bestbusinesses.space/sitemap.xml",
#     "https://bestbusinesses.space/random-sitemap.xml",
#     "https://bestbusinesses.space/random-sitemap.xml", 
#     'https://bestbusinesses.space/random-sitemap.xml', 
#     'https://bestbusinesses.space/random-sitemap.xml', 
#     'https://bestbusinesses.space/random-sitemap.xml', 
#     'https://sitemap.bestbusinesses.space/sitemap.xml', 
#     "https://ustopbusiness.online/sitemap.xml",
#     "https://ustopbusiness.online/random-sitemap.xml",
#     "https://ustopbusiness.online/random-sitemap.xml", 
#     'https://ustopbusiness.online/random-sitemap.xml', 
#     'https://ustopbusiness.online/random-sitemap.xml', 
#     'https://ustopbusiness.online/random-sitemap.xml', 
#     'https://sitemap.ustopbusiness.online/sitemap.xml', 
#     "https://americantopbusiness.site/sitemap.xml",
#     "https://americantopbusiness.site/random-sitemap.xml",
#     "https://americantopbusiness.site/random-sitemap.xml", 
#     'https://americantopbusiness.site/random-sitemap.xml', 
#     'https://americantopbusiness.site/random-sitemap.xml', 
#     'https://americantopbusiness.site/random-sitemap.xml', 
#     'https://sitemap.americantopbusiness.site/sitemap.xml',
#     "https://americanbusinesses.space/sitemap.xml",
#     "https://americanbusinesses.space/random-sitemap.xml",
#     "https://americanbusinesses.space/random-sitemap.xml", 
#     'https://americanbusinesses.space/random-sitemap.xml', 
#     'https://americanbusinesses.space/random-sitemap.xml', 
#     'https://americanbusinesses.space/random-sitemap.xml', 
#     'https://sitemap.americanbusinesses.space/sitemap.xml'
# ]

urls = ["https://gnews.io/sitemap.xml", 
        "https://gnews.io/sitemap.xml", 
        "https://gnews.io/sitemap.xml"
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

# Define log file path
log_file_path = '/var/indexing/fastindexing.log'

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

# Set up logging (we will override the basicConfig later to write logs to the file)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Custom logging handler to prepend logs
class PrependFileHandler(logging.Handler):
    def emit(self, record):
        log_message = self.format(record)
        prepend_log_to_file(log_message)

# Attach the custom handler to the logger
prepend_handler = PrependFileHandler()
logger.addHandler(prepend_handler)

# Function to push the log file to GitHub
def push_log_to_github():
    try:
        # Change to the directory of your Git repository
        os.chdir('/var/indexing')  # Path to your GitHub repo

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
def wait_until_loaded(driver, max_wait_time=300):
    logger.info("Waiting for the page to finish loading...")
    WebDriverWait(driver, max_wait_time).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )
    logger.info("Page has finished loading.")

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

# Main function
def process_urls():
    # Add the current date and time as a header at the top of the log file
    log_title = f"Processing started at: {time.strftime('%Y-%m-%d %H:%M:%S')}"
    prepend_log_to_file(log_title)  # Prepend the title to the log file

    for url in urls:
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
            
        except Exception as e:
            logger.error(f"An error occurred while processing the URL {url}: {e}")
        
        # Refresh the page before going to the next URL
        driver.refresh()
        logger.info("Page refreshed after submission.")
        
        # Wait a little before moving on to the next URL
        time.sleep(5)  # Adjust the delay as needed
        logger.info("Waiting before processing the next URL...\n")
    
    # After processing all URLs, push the log to GitHub
    push_log_to_github()

# Run the script once (this will be called by the cron job)
try:
    process_urls()
except Exception as e:
    logger.error(f"An error occurred: {e}")
finally:
    # Close the browser after processing all URLs
    logger.info("Closing the browser.")
    driver.quit()