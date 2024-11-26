from get_cgpa import scan_result_dir, fix_coloumn
from openpyxl import load_workbook
import pandas as pd
import math

# Path to the Excel file
file_path = "data/2BCA-A.xlsx"  # Replace with your input file path
newfile_path = "data/2BCA-A-updated.xlsx" # Rename output file
sheet_name = "tablexls"       # Replace with the sheet name you want to read (inside excel)

result_dir = r"C:\Users\sanjay\Downloads\Results\2BCA-A"

def is_nan(value):
    """Check if a value is NaN."""
    return isinstance(value, float) and math.isnan(value)


def read_and_write():
    '''
        reads and write excel sheet with updated data 
    '''

    try:
        # Provide path for folder containing csjmu results
        result_data = scan_result_dir(result_dir)

        data = pd.read_excel(file_path, sheet_name=sheet_name)

        # Add missing columns if necessary
        for col in ['CGPA', 'BP', 'Result', 'Division']:
            if col not in data.columns:
                data[col] = None

        first_key, first_value = next(iter(result_data.items()))

        sem_count = len(first_value)

        for sem in range(1, sem_count + 1):
            col_name = f"sem{sem}_sgpa"
            if col_name not in data.columns:
                data[col_name] = None

        # Ensure the 'Result' column can hold strings
        data['Result'] = data['Result'].astype('object')  # or 'string' for newer versions of Pandas

        # Ensure the 'BP' column can hold strings
        data['BP'] = data['BP'].astype('object')  # or 'string'
        
        for index, row in data.iloc[1:].iterrows():
            # Accessing data in each row

            roll_number = row['Roll Number']

            data.at[index, 'CGPA'] = 0.0
            data.at[index, 'BP'] = None
            data.at[index, 'Result'] = None
            data.at[index, 'Division'] = None
            
            if is_nan(roll_number):
                continue


            if str(int(roll_number)) in result_data:
                my_result_data = result_data[str(int(roll_number))]
                

                # Assign SGPA data dynamically
                for sem_index, sem_data in enumerate(my_result_data):
                    sem_col = f"sem{sem_index + 1}_sgpa"
                    if sem_col in data.columns:
                        data.at[index, sem_col] = sem_data.get("sgpa", None)

                last_sem_data = my_result_data[-1]
                data.at[index, 'CGPA'] = last_sem_data.get("cgpa", None)
                data.at[index, 'BP'] = ",".join(last_sem_data["back_papers"]) if last_sem_data.get("back_papers") else None
                data.at[index, 'Result'] = last_sem_data.get("result", None)
                data.at[index, 'Division'] = last_sem_data.get("division", None)
                  
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