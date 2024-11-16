import os
import time
import pandas as pd
import fitz  # PyMuPDF

data = []

def getScore(pdf_path):
    # print(pdf_path)
    with fitz.open(pdf_path) as pdf:
        # Iterate through the pages (starting from the second page)
        for page_number in range(0, len(pdf)):  # Start from the second page
            page = pdf.load_page(page_number)
            text = page.get_text("text")

            # Split the text into lines and look for the row with "SGPA"
            lines = text.split('\n')

            for i, line in enumerate(lines):
                if "SGPA" in line:
                    sgpa = lines[i+1]
                    
                if "CGPA" in line:
                    cgpa = lines[i+1]


        data.append([str(pdf_path), sgpa, cgpa])


def getToppers(folder_name):
    start_time = time.time()

    for filename in os.listdir(folder_name):
        file_path = os.path.join(folder_name, filename)
        if os.path.isfile(file_path):
            getScore(file_path)
            

    end_time = time.time()

    elapsed = end_time - start_time
    print(f"Elapsed time: {elapsed:.2f} seconds")

    # Sort by CGPA
    data_sorted = sorted(data, key=lambda x: float(x[2]), reverse=True)

    print("Top 10 Toppers:")
    for entry in data_sorted[:10]:
        print(entry)

    # Convert sorted data to a DataFrame
    df = pd.DataFrame(data_sorted[:10], columns=['File Path', 'SGPA', 'CGPA'])

    # Save to Excel file
    df.to_excel(f"{folder_name}-toppers.xlsx", index=False)
    print("Data saved to toppers.xlsx")


if __name__ == "__main__":
    getToppers(folder_name=r"C:\Users\sanjay\Downloads\Results\2BCA-A")
