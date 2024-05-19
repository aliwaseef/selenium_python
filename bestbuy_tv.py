# Importing necessary libraries for web scraping and automation.
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Specify the location of the ChromeDriver, which allows Selenium to control Chrome.
# service = Service(executable_path='path_to_your_chromedriver')

# Specify the path to chromedriver.exe
service = Service(executable_path='C:/path/to/chromedriver.exe')

# Initialize the Chrome browser session using the specified service.
driver = webdriver.Chrome(service=service)

# Directs the browser to open the URL for Best Buy's homepage.
driver.get("https://www.bestbuy.ca")

# Maximizes the browser window to ensure visibility of all web elements.
driver.maximize_window()

# Pause the script for 5 seconds to allow the web page to load completely.
time.sleep(5)

# Attempt to find and close any popup that might block further interactions.
try:
    close_popup = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".c-modal-close-icon"))
    )
    close_popup.click()
except:
    print("No popup found")

# Locate the search input field by its ID and prepare to enter a query.
search_bar = driver.find_element(By.ID, "gh-search-input")
search_bar.clear()  # Clears any pre-existing text in the search bar.
search_bar.send_keys("75-inch TV")  # Types the search query into the search bar.
search_bar.send_keys(Keys.RETURN)  # Simulates pressing the Enter key to submit the search.

# Wait until the search results are visible on the new page.
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, ".sku-header"))
)

# Filter the search result by 'On Sale'
on_sale_checkbox = driver.find_element('') # add the element mapping
driver.execute_script("argument[0].scrollIntoView();", on_sale_checkbox)
on_sale_checkbox.click()

# Gather all elements that represent individual TV listings on the search results page.
tvs = driver.find_elements(By.CSS_SELECTOR, ".sku-item")
for tv in tvs:
    # Click and open each listing
    
    # Extract and print the TV title from each listing.
    title = tv.find_element(By.CSS_SELECTOR, ".sku-header a").text
    try:
        # Attempt to extract the price; if not present, set a default message.
        price = tv.find_element(By.CSS_SELECTOR, ".priceView-customer-price span").text
    except:
        price = "No price listed"
    
    try:
        # Attempt to extract sales end date information; format it if present.
        sales_end = tv.find_element(By.CSS_SELECTOR, ".priceView-price-messaging span").text
        if "Ends" in sales_end:
            sales_end_date = sales_end.split("Ends ")[1]
        else:
            sales_end_date = "No specific end date"
    except:
        sales_end_date = "No sales information"

    # Return to previous page
    
    # Output the information for each TV to the console.
    print(f"TV: {title}, Price: {price}, Sales End Date: {sales_end_date}")

# Close the browser after completing all operations.
driver.quit()
