import os
import time
from openpyxl import load_workbook

import fitz  # PyMuPDF


def scan_result_dir(base_folder):
    """
    Traverse the directory structure and collect all semester data for each roll number.

    Base_Folder/
            1/
                12345.pdf
                67890.pdf
            2/
                12345.pdf
                67890.pdf
            3/
                12345.pdf

    """
    all_data = {}

    start_time = time.time()
    # Loop through each semester folder in the base directory
    for semester in sorted(os.listdir(base_folder), key=lambda x: int(x)):  # Sort semesters numerically
        sem_path = os.path.join(base_folder, semester)
        if os.path.isdir(sem_path):
            for pdf_file in os.listdir(sem_path):
                if pdf_file.endswith(".pdf"):
                    filename = pdf_file.split(".")[0]  # Extract roll number from file name
                    roll_number = filename.split('-')[-1]

                    if roll_number not in all_data:
                        all_data[roll_number] = []
                    
                    pdf_path = os.path.join(sem_path, pdf_file)
                    pdf_data = read_csjmu_result(pdf_path)
                    
                    if pdf_data:
                        # Append semester data (file path) to the roll number list
                        all_data[roll_number].append({
                            "semester": semester,
                            "sgpa": pdf_data[2],
                            "cgpa": pdf_data[3],
                            "back_papers": pdf_data[4],
                            "result": pdf_data[5],
                            "division": pdf_data[6],
                            "pdf_path": pdf_data[0]
                        })
    end_time = time.time()
    elapsed = end_time - start_time
    
    print(f"Elapsed time: {elapsed:.2f} seconds - Scanning Done!")
    return all_data




def read_csjmu_result(pdf_path):
    '''
       Extract data from result pdf
        Supported: CSJMU RESULT ONLY
    '''

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
                    if lines[i+1] == "SGPA":
                        back_papers = None
                    else:    
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


    return [
            str(pdf_path), 
            int(roll_number), 
            float(sgpa), 
            float(cgpa), 
            back_papers if back_papers else None, 
            result, 
            division
        ]



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

    data = scan_result_dir(r"C:\Users\sanjay\Downloads\Results\2BCA-A")
    print(data)