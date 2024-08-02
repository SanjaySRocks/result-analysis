# CSJMU Result Downloader
A python tool to download result from csjmu official website


```
python main.py
```

### Installation
```
pip install selenium webdriver-manager
```

## Usage:

1. Get student result by name, rollno, dob

```
result = CSJMUResult()
result.process_student("MANASVI MISHRA", 22015003575, "05/27/2006")
result.close()
```

2. Get all result by providing a list of students

```
result = CSJMUResult()
result.get_all_students()
result.close()
```

3. Get roll number from enrollment number

```
result = CSJMUResult()
roll_number = result.get_roll_no("CSJMA22001670707")
print(roll_number)
result.close()
```


