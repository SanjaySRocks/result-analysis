import pdfplumber
import os
import time
# pdf_path = 'Results/result-MANASVI_MISHRA-22015003575.pdf'
import pandas as pd

data = []

def getScore(pdf_path):
    print(pdf_path)
    with pdfplumber.open(pdf_path) as pdf:
        for page_number in range(0, len(pdf.pages)):  # Start from the second page
            page = pdf.pages[page_number]
            table = page.extract_table()

            if table:
                for row in table:
                    if row[0] == "SGPA":
                        data.append([str(pdf_path), row[2], row[5]])


def getToppers(folder_name):
    start_time = time.time()

    for filename in os.listdir(folder_name):
        file_path = os.path.join(folder_name, filename)
        if os.path.isfile(file_path):
            getScore(file_path)

    end_time = time.time()

    elapsed = end_time - start_time
    print(elapsed)

    # Sort by CGPA
    data_sorted = sorted(data, key=lambda x: float(x[2]), reverse=True)

    print("Top 10 Toppers:")
    for entry in data_sorted[:10]:
        print(entry)

    # Convert sorted data to a DataFrame
    df = pd.DataFrame(data_sorted[:10], columns=['File Path', 'SGPA', 'CGPA'])

    # Save to Excel file
    df.to_excel("{}-toppers.xlsx".format(folder_name), index=False)
    print("Data saved to toppers.xlsx")


if __name__=="__main__":
    getToppers(folder_name="2BCA-A")