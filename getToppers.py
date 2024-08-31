import pdfplumber
import os
import time
# pdf_path = 'Results/result-MANASVI_MISHRA-22015003575.pdf'

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


def main():
    start_time = time.time()

    for filename in os.listdir("Results"):
        file_path = os.path.join("Results", filename)
        if os.path.isfile(file_path):
            getScore(file_path)

    end_time = time.time()

    elapsed = end_time - start_time
    print(elapsed)

    data_sorted = sorted(data, key=lambda x: float(x[2]), reverse=True)

    print(data_sorted[:3])

main()