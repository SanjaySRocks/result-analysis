from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException

import edgedriver_autoinstaller
import os, json
import base64

baseDetails = {
    "sessionId": "24",
    "category": "RG",
    "course": "BACHELOR OF COMPUTER APPLICATION",
    "sem": "4"
}


with open("students.json", 'r') as file:
    Students = json.load(file)


class CSJMUResult():
    def __init__(self):
        edgedriver_autoinstaller.install()

        self.edge_options = Options()
        self.edge_options.add_argument('--kiosk-printing')
        self.edge_options.add_argument('--log-level=3')
        self.edge_options.add_argument("--headless")
        self.edge_options.add_argument("--disable-gpu")
        self.edge_options.add_argument("--no-sandbox")
        self.edge_options.add_argument("--guest")

        self.driver = webdriver.Edge(options=self.edge_options)
    
    def get_all_students(self):
        for st in Students:
            self.process_student(st['name'], st['rollno'], st['dob'])


    def process_student(self, name, rollno, dob):
        try:
            # Open CSJMU Website
            self.driver.get("https://admission.csjmu.ac.in/DisplayResult/Index")

            # Fill session id
            dropdown_sessionid = self.driver.find_element(By.ID, "SessionID")
            select = Select(dropdown_sessionid)
            select.select_by_value(baseDetails['sessionId'])

            # Wait for api to populate exam category
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//option[@value='{baseDetails['category']}']"))
            )

            dropdown_examcode = self.driver.find_element(By.ID, "ExamCategoryCode")
            select = Select(dropdown_examcode)
            select.select_by_value(baseDetails['category'])


            # wait for api to populate course options
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//option[text()='{baseDetails['course']}']"))
            )
            
            # click on course option
            dropdown_course = self.driver.find_element(By.XPATH, "//span[@id='select2-SubCourseID-container']")
            dropdown_course.click()

            # wait and click on course 
            dropdown_option = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, f"//li[@class='select2-results__option' and text()='{baseDetails['course']}']")))
            dropdown_option.click()
            
            
            # wait for api to populate semester option
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//option[@value='{baseDetails['sem']}']"))
            )

            dropdown_sem = self.driver.find_element(By.ID, "SemYearID")
            select = Select(dropdown_sem)
            select.select_by_value(baseDetails['sem'])


            # Fill rollno
            rollno_input = self.driver.find_element(By.ID, "StRollNo")
            rollno_input.send_keys(rollno)

            # Fill date 
            date_input = self.driver.find_element(By.ID, "StDOB")
            date_input.send_keys(dob)

            
            # Wait for button to appear and click
            view_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "btn-primary"))
            )
            view_button.click()

            # Wait for print button and save the result
            print_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@type='button' and @value='Print Result']"))
            )

            if print_button:
                # print(True)
                format_name = name.replace(' ', '_')
                self.save_as_pdf(f"Results/result-{format_name}-{rollno}.pdf")
                print(f"---- Download Result Pdf!! {name} ----")
            

        except UnexpectedAlertPresentException as e:
            print(e)

        except Exception as e:
            print(f"An error occurred: {e}")

    
    def save_as_pdf(self, path):
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
        result = self.driver.execute_cdp_cmd("Page.printToPDF", print_options)
        
        # Decode the base64-encoded PDF data
        pdf_data = base64.b64decode(result['data'])
        
        # Write the PDF to a file
        with open(path, 'wb') as file:
            file.write(pdf_data)

    def close(self):
        self.driver.quit()
    
    # Extra functions
    def get_roll_no(self, enrollno):
        try:
            # Open the website
            self.driver.get("https://admission.csjmu.ac.in/Search/SearchRollNumber")


            # Find the input field by ID and enter a value
            enrolment_field = self.driver.find_element(By.ID, "EnrolmentNo")
            enrolment_field.send_keys(enrollno)  # Replace with the actual value


            # Find the search button by ID and click it
            search_button = self.driver.find_element(By.ID, "btnSearch")
            search_button.click()

            # Wait for results or further actions
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table.table.table-sm"))
            )

            table = self.driver.find_element(By.CSS_SELECTOR, "table.table.table-sm")
            cells = table.find_elements(By.TAG_NAME, "td")

            # The roll number should be in the second cell
            roll_number = cells[0].text

            return roll_number

        except Exception as e:
            print(f"An error occurred: {e}")
            return None


if __name__=="__main__":
    result = CSJMUResult()
    # result.process_student("MANASVI MISHRA", 22015003575, "05/27/2006")
    result.get_all_students()
    result.close()