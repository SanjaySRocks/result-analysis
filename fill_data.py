from get_cgpa import getScore, getStudentData, fix_coloumn
from openpyxl import load_workbook
import pandas as pd

# Path to the Excel file
file_path = "data/3BCA-A.xlsx"  # Replace with your input file path
newfile_path = "data/3BCA-A-updated.xlsx" # Rename output file
sheet_name = "tablexls"       # Replace with the sheet name you want to read (inside excel)


def read_and_write():
    '''
        reads and write excel sheet with updated data 
    '''
    # Provide path for folder containing csjmu results
    six_data = getStudentData(folder_name=r"C:\Users\sanjay\Downloads\Results\3BCA-A")
    # fourth_data = getStudentData(folder_name=r"C:\Users\sanjay\Downloads\Results\2BCA-A")
    # third_data = getStudentData(folder_name=r"C:\Users\sanjay\Downloads\Results\2BCA-A_3rdSem")
    # second_data = getStudentData(folder_name=r"C:\Users\sanjay\Downloads\Results\1BCA-B")
    # first_data = getStudentData(folder_name=r"C:\Users\sanjay\Downloads\Results\2BCA-A_1stSem")
    
    # Read the Excel file
    try:
        data = pd.read_excel(file_path, sheet_name=sheet_name)

        if 'Division' not in data.columns:
            data['Division'] = None

        # Print the content of the DataFrame
        print("Excel Sheet Content:")
        for index, row in data.iloc[1:].iterrows():
            # Accessing data in each row
            roll_number = row['Roll Number']
            name = row['Full Name']

            data.at[index, 'CGPA'] = 0.0
            data.at[index, 'BP'] = None
            data.at[index, 'Result'] = None
            data.at[index, 'Division'] = None
            
            filtered_record = [record for record in six_data if record[1] == roll_number]
            print(filtered_record)
            if len(filtered_record) > 0:
                data.at[index, 'CGPA'] = filtered_record[0][3]
                data.at[index, 'BP'] = ",".join(filtered_record[0][4]) if filtered_record[0][4] is not None else None
                data.at[index, 'Result'] = filtered_record[0][5]
                data.at[index, 'Division'] = filtered_record[0][6] if filtered_record[0][6] is not None else None
               

            cgpa = data.at[index, 'CGPA']
            
            # print(f"Row {index}: Roll Number: {roll_number}, Name: {name}, CGPA: {cgpa}")
        
        if input("Confirm writing excel sheet? (y/n): ").lower() == 'y':
            data.to_excel(newfile_path, index=False)
            fix_coloumn(newfile_path)
            print(" File written successfully!")
        else:
            print("Operation Canceled")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    read_and_write()