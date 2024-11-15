from main import CSJMUResult, AKTUResult


result = CSJMUResult()
result.read_excel_sheet(filename="1BCA-A.xlsx")
result.get_all_students()
result.close()