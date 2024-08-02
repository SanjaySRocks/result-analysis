from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")  # Optional: Might help in some environments
chrome_options.add_argument("--disable-dev-shm-usage")  # Optional: Might help in some environments

# Set up ChromeDriver service
service = Service(ChromeDriverManager().install())

# Initialize WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open a webpage
driver.get('https://www.google.com')

# Print the title of the webpage
print(driver.title)

# Close the WebDriver
driver.quit()
