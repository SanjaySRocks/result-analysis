from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException

import edgedriver_autoinstaller
import os
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

Students = [{'name': 'NILESH KUMAR ', 'rollno': 22015003581, 'dob': '03/10/2006'}, {'name': 'SHALINI SINGH', 'rollno': 22015003600, 'dob': '11/28/2000'}, {'name': 'KARTIKAY GAUTAM', 'rollno': 22015003570, 'dob': '07/27/2005'}]


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

def run():
    try:
        for st in Students:
            try:
                # Open CSJMU Website
                driver.get("https://admission.csjmu.ac.in/DisplayResult/Index")

                # Fill session id
                dropdown_sessionid = driver.find_element(By.ID, "SessionID")
                select = Select(dropdown_sessionid)
                select.select_by_value(baseDetails['sessionId'])

                # Wait for api to populate exam category
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, f"//option[@value='{baseDetails['category']}']"))
                )

                dropdown_examcode = driver.find_element(By.ID, "ExamCategoryCode")
                select = Select(dropdown_examcode)
                select.select_by_value(baseDetails['category'])


                # wait for api to populate course options
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, f"//option[text()='{baseDetails['course']}']"))
                )
                
                # click on course option
                dropdown_course = driver.find_element(By.XPATH, "//span[@id='select2-SubCourseID-container']")
                dropdown_course.click()

                # wait and click on course 
                dropdown_option = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f"//li[@class='select2-results__option' and text()='{baseDetails['course']}']")))
                dropdown_option.click()
                
                
                # wait for api to populate semester option
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, f"//option[@value='{baseDetails['sem']}']"))
                )

                dropdown_sem = driver.find_element(By.ID, "SemYearID")
                select = Select(dropdown_sem)
                select.select_by_value(baseDetails['sem'])


                # Fill rollno
                rollno_input = driver.find_element(By.ID, "StRollNo")
                rollno_input.send_keys(st['rollno'])

                # Fill date 
                date_input = driver.find_element(By.ID, "StDOB")
                date_input.send_keys(st['dob'])

                
                # Wait for button to appear and click
                view_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "btn-primary"))
                )
                view_button.click()

                # Wait for print button and save the result
                print_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@type='button' and @value='Print Result']"))
                )

                if print_button:
                    # print(True)
                    save_as_pdf(driver, f"Results/result-{st['rollno']}.pdf")
                    print(f"---- Download Result Pdf!! {st['rollno']} ----")
                

            except UnexpectedAlertPresentException as e:
                print(e)

            except Exception as e:
                print(f"An error occurred: {e}")


    finally:
        # Close the browser
        driver.quit()



if __name__=="__main__":
    run()