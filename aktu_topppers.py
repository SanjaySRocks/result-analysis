import pdfplumber
import os
import time
# pdf_path = 'Results/result-MANASVI_MISHRA-22015003575.pdf'
import pandas as pd

data = []

def getScore(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            # print(text)
            # Search for keywords related to CGPA
            keywords = ["CGPA", "Cumulative Grade Point Average"]
            for keyword in keywords:
                if keyword in text:
                    # Extract the line containing the CGPA
                    cgpa_line = text.split(keyword)[1].strip()
                    # # Extract the CGPA value, assuming it's a number
                    cgpa_str = cgpa_line.split()[1]
                    cgpa = float(cgpa_str)
                    print(pdf_path, cgpa)
                    data.append([str(pdf_path), cgpa])


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
    data_sorted = sorted(data, key=lambda x: float(x[1]), reverse=True)

    print("Top 10 Toppers:")
    for entry in data_sorted[:10]:
        print(entry)

    # Convert sorted data to a DataFrame
    df = pd.DataFrame(data_sorted[:10], columns=['File Path', 'CGPA'])

    # Save to Excel file
    df.to_excel("{}-toppers.xlsx".format(folder_name), index=False)
    print("Data saved to toppers.xlsx")


if __name__=="__main__":
    getToppers(folder_name="1MCA-A")