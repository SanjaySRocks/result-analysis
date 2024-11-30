import pandas as pd
import json

def extract_data_from_excel(file_path, fullname_col, rollno_col, dob_col):
    df = pd.read_excel(file_path)

    # Check if all required columns are present
    required_columns = [fullname_col, rollno_col, dob_col]
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        print(f"The following columns are missing in the Excel file: {missing_columns}")
        return []
    
    # print(df.columns)
    data = []
    for index, row in df.iterrows():
        # print(row)
        roll_number = row.get(rollno_col)
        name = row.get(fullname_col)
        dob = row.get(dob_col)

        # print(rollno_col, roll_number, name, dob)
        if pd.notna(roll_number) and pd.notna(name) and pd.notna(dob):
            
            if not isinstance(dob, pd.Timestamp):
                try:
                    dob = pd.to_datetime(dob, errors='coerce')
                except Exception as e:
                    print(f"Error converting date for row {row}: {e}")
                    dob = None

            # Format dob if conversion was successful
            # if csjmu '%m/%d/%Y'
            # if aktu '%d/%m/%Y'
            dob_str = dob.strftime('%d/%m/%Y') if pd.notna(dob) else "Invalid Date"
            

            data.append({
                'name': name,
                'rollno': int(roll_number),
                'dob': dob_str
            })
    return data