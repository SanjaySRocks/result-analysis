from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException

import edgedriver_autoinstaller
import time, os
import base64

edgedriver_autoinstaller.install()

# Set up Edge options for headless mode
edge_options = Options()
edge_options.add_argument('--kiosk-printing')
edge_options.add_argument("--headless")
edge_options.add_argument("--disable-gpu")

# Initialize the Edge WebDriver with the headless options
driver = webdriver.Edge(options=edge_options)

baseDetails = {
    "sessionId": "24",
    "category": "RG",
    "course": "BACHELOR OF COMPUTER APPLICATION",
    "sem": "4"
}

Students = [
    {
        "rollno": "22015003570",
        "dob": "07/27/2005" # Month/Day/Year
    },
    {
        "rollno": "22015003600",
        "dob": "11/28/2000" # Month/Day/Year
    }
]


def save_as_pdf(driver, path):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    print_options = {
        'landscape': False,
        'displayHeaderFooter': False,
        'printBackground': True,
        'preferCSSPageSize': True
    }

    # Convert the page to PDF
    result = driver.execute_cdp_cmd("Page.printToPDF", print_options)
    
    # Decode the base64-encoded PDF data
    pdf_data = base64.b64decode(result['data'])
    
    # Write the PDF to a file
    with open(path, 'wb') as file:
        file.write(pdf_data)

try:
    for st in Students:
        try:
            # Open Google Shopping
            driver.get("https://admission.csjmu.ac.in/DisplayResult/Index")


            dropdown_sessionid = driver.find_element(By.ID, "SessionID")
            select = Select(dropdown_sessionid)
            select.select_by_value(baseDetails['sessionId'])

            time.sleep(1)

            dropdown_examcode = driver.find_element(By.ID, "ExamCategoryCode")
            select = Select(dropdown_examcode)
            select.select_by_value(baseDetails['category'])

            time.sleep(1)
        
            dropdown = driver.find_element(By.XPATH, "//span[@id='select2-SubCourseID-container']")
            dropdown.click()

            wait = WebDriverWait(driver, 10)
            option = wait.until(EC.visibility_of_element_located((By.XPATH, f"//li[@class='select2-results__option' and text()='{baseDetails['course']}']")))
            option.click()
            
            time.sleep(1)

            dropdown_examcode = driver.find_element(By.ID, "SemYearID")
            select = Select(dropdown_examcode)
            select.select_by_value(baseDetails['sem'])


            time.sleep(1)

            date_input = driver.find_element(By.ID, "StRollNo")
            date_input.send_keys(st['rollno'])

            time.sleep(1)

            date_input = driver.find_element(By.ID, "StDOB")
            date_input.send_keys(st['dob'])

            time.sleep(1)

            view_button = driver.find_element(By.CLASS_NAME, "btn-primary")
            view_button.click()

            print_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='button' and @value='Print Result']"))
        )

            if print_button:
                print(True)
                save_as_pdf(driver, f"Results/result-{st['rollno']}.pdf")
                print(f"---- Download Result Pdf!! {st['rollno']} ----")
            

        except UnexpectedAlertPresentException as e:
            print(e)

        except Exception as e:
            print(f"An error occurred: {e}")


finally:
    # Close the browser
    driver.quit()
