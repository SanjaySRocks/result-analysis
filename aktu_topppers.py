import fitz  # PyMuPDF
import os
import time
import pandas as pd

data = []

# Function to extract CGPA from a PDF using PyMuPDF
def getScore(pdf_path):
    local_data = []  # To store results of this process

    doc = fitz.open(pdf_path)
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)  # Load a page
        text = page.get_text("text")  # Extract plain text from the page
        
        # Search for keywords related to CGPA
        keywords = ["CGPA", "Cumulative Grade Point Average"]
        for keyword in keywords:
            if keyword in text:
                # Extract the line containing the CGPA
                cgpa_line = text.split(keyword)[1].strip()
                # Extract the CGPA value, assuming it's a number
                cgpa_str = cgpa_line.split()[1]
                cgpa = float(cgpa_str)
                local_data.append([str(pdf_path), cgpa])
    
    return local_data  # Return local results

# Function to process PDFs in a folder
def getToppers(folder_name):
    start_time = time.time()

    # Prepare the list of PDF file paths to be processed
    pdf_files = [os.path.join(folder_name, filename) for filename in os.listdir(folder_name) if os.path.isfile(os.path.join(folder_name, filename))]

    # Process each PDF file sequentially (no multiprocessing)
    for pdf_path in pdf_files:
        local_data = getScore(pdf_path)  # Get the score for each file
        data.extend(local_data)  # Add the results to the global data list

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

    end_time = time.time()
    elapsed = end_time - start_time
    print(f"Elapsed time: {elapsed} seconds")

if __name__ == "__main__":
    # Use the correct folder path for your system
    folder_path = r"C:\Users\sanjay\Downloads\Results\2MCA-A"
    getToppers(folder_name=folder_path)
