from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException

#Edge Driver
# from selenium.webdriver.edge.service import Service as EdgeService
# from selenium.webdriver.edge.options import Options
# from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Chrome Driver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import os, json
import base64
import time

baseDetails = {
    "sessionId": "24",
    "category": "RG",
    "course": "BACHELOR OF COMPUTER APPLICATION",
    "sem": "4"
}


class BaseResult:
    def __init__(self):

        self.driver_options = Options()
        self.driver_options.add_argument('--kiosk-printing')
        self.driver_options.add_argument('--log-level=3')
        self.driver_options.add_argument('--guest')
        self.driver_options.add_argument("--disable-dev-shm-usage")
        self.driver_options.add_argument("--no-sandbox")
        self.driver_options.add_argument("--headless")
        self.driver_options.add_argument("--disable-gpu")

        # self.service = EdgeService(EdgeChromiumDriverManager().install())
        # self.driver = webdriver.Edge(service=self.service, options=self.driver_options)

        self.service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service, options=self.driver_options)

    
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

    def check_result_exist(self, name, rollno, result_folder):
        format_name = name.replace(' ', '_')
        result_path = f"{result_folder}/result-{format_name}-{rollno}.pdf"
        if os.path.exists(result_path):
            print(f"The file '{result_path}' already exists.")
            return True
        return False

    def close(self):
        self.driver.quit()


class CSJMUResult(BaseResult):    
    def get_all_students(self):

        with open("students.json", 'r') as file:
            Students = json.load(file)

        for st in Students:
            self.process_student(st['name'], st['rollno'], st['dob'])


    def process_student(self, name, rollno, dob):

        if self.check_result_exist(name, rollno, "Results"):
            return

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

            details = f"---- Failed to Get Pdf!! {name} {rollno} {dob} ----"
            print(details)
            print("Error: ", e.alert_text)

            with open('error_logs', 'a') as file:
                file.write(f'{details}\nError: {e.msg}\n\n')


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



class AKTUResult(BaseResult):
    def get_all_students(self):
        with open("aktustudents.json", 'r') as file:
            Students = json.load(file)

        for st in Students:
            self.process_student(st['name'], st['rollno'], st['dob'])


    def process_student(self, name, rollno, dob):
        
        if self.check_result_exist(name, rollno, "AKTUResults"):
            return
    
        try:
            self.driver.get("https://oneview.aktu.ac.in/WebPages/aktu/OneView.aspx")

            self.roll_input = self.driver.find_element(By.ID, 'txtRollNo')
            self.roll_input.send_keys(rollno)

            self.submit_btn = self.driver.find_element(By.ID, 'btnProceed')
            self.submit_btn.click()

            input_dob = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'txtDOB'))
            )

            input_dob.send_keys(dob)

            input_dob.send_keys(Keys.RETURN)

            # self.submit_btn = WebDriverWait(self.driver, 10).until(
            #     EC.element_to_be_clickable((By.ID, 'btnSearch'))
            # )
            # self.submit_btn.click()

            # Result Page Open
            # result_page = WebDriverWait(self.driver, 10).until(
            #     EC.visibility_of_element_located((By.ID, 'lblRollNo'))
            # )

            # if result_page:
            self.scroll_expand()

            format_name = name.replace(' ', '_')
            self.save_as_pdf(self.driver, f"AKTUResults/result-{format_name}-{rollno}.pdf")

            print(f"---- Download Result Pdf!! {name} ----")

        except Exception as e:
            details = f"---- Failed to Get Pdf!! {name} {rollno} {dob} ----"
            
            print(details)
            print("An error occurred: ", e.msg)

            with open('aktu_error_logs', 'a') as file:
                file.write(f'{details}\nError: {e}\n\n')


    def scroll_expand(self):
        self.elements = self.driver.find_elements(By.CLASS_NAME, 'headerclass')

        for index, element in enumerate(self.elements):
            try:
                # Scroll the element into view
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                
                # Wait until the element is visible and clickable
                WebDriverWait(self.driver, 10).until(
                    EC.visibility_of(element)
                )
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, 'headerclass'))
                )
                
                element.click()
                
                time.sleep(0.5)
                
            except Exception as e:
                print(f"An error occurred while clicking element {index+1}: {e}")



if __name__=="__main__":
    result = CSJMUResult()
    result.process_student("MANASVI MISHRA", 22015003575, "05/27/2006")
    # result.get_all_students()
    result.close()

    # result = AKTUResult()
    # result.get_all_students()
    # result.close()