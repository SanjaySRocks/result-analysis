import os
import time
import pandas as pd
from openpyxl import load_workbook

import fitz  # PyMuPDF


def getScore(pdf_path):
    '''
        Takes result pdf path as argument
        returns extracted data from pdf
        Supported: CSJMU RESULT ONLY
    '''
    local_data = []
    # print(pdf_path)
    back_papers = None
    result = None
    division = None

    with fitz.open(pdf_path) as pdf:
        # Iterate through the pages (starting from the second page)
        for page_number in range(0, len(pdf)):  # Start from the second page
            page = pdf.load_page(page_number)
            text = page.get_text("text")

            # print(text)
            # Split the text into lines and look for the row with "SGPA"
            lines = text.split('\n')
            # print(lines)
            for i, line in enumerate(lines):
                # print(line)

                if "ROLL NO." in line:
                    roll_number = lines[i+1]

                if "CARRY OVER PAPER(S)" in line:
                    back_papers = lines[i+1].split(",")

                if "RESULT" == line:
                    # print(line)
                    result = lines[i+1]

                if "DIVISION" == line and result == "PASSED":
                    division = lines[i+1]

                if "SGPA" in line:
                    sgpa = lines[i+1]
                    
                if "CGPA" in line:
                    cgpa = lines[i+1]


    local_data.append([str(pdf_path), int(roll_number), float(sgpa), float(cgpa), back_papers if back_papers else None, result, division])
    
    return local_data



def getStudentData(folder_name):
    '''
        It takes result folder path as arguement
        returns all pdf extracted data as an list
    '''
    data = []
    start_time = time.time()

    for filename in os.listdir(folder_name):
        file_path = os.path.join(folder_name, filename)
        if os.path.isfile(file_path):
            data.extend(getScore(file_path))
            
    end_time = time.time()
    elapsed = end_time - start_time
    
    print(f"Elapsed time: {elapsed:.2f} seconds")

    return data

    



def fix_coloumn(excel_file):
    '''
        Fix coloumn width automatically
        Pass excel file path as argument
    '''
    wb = load_workbook(excel_file)
    ws = wb.active

    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter  # Get the column letter
        for cell in column:
            try:  # Ignore empty cells
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            except:
                pass
        adjusted_width = max_length + 2  # Add some padding
        ws.column_dimensions[column_letter].width = adjusted_width

    # Save the adjusted Excel file
    wb.save(excel_file)


if __name__ == "__main__":
    # fourth_data = getStudentData(folder_name=r"C:\Users\sanjay\Downloads\Results\2BCA-A")
    # third_data = getStudentData(folder_name=r"C:\Users\sanjay\Downloads\Results\2BCA-A_3rdSem")
    # second_data = getStudentData(folder_name=r"C:\Users\sanjay\Downloads\Results\2BCA-A_2ndSem")
    # first_data = getStudentData(folder_name=r"C:\Users\sanjay\Downloads\Results\2BCA-A_1stSem")
    
    # for fd in fourth_data:
    #     print(fd)

    # filtered_data = [record for record in fourth_data if record[1] == 22015003610]
    # print(filtered_data)

    print(getScore("C:\\Users\\sanjay\\Downloads\\Results\\3BCA-A\\result-VIVEK__SINGH-21015002607.pdf"))
