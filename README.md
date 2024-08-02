# CSJMU Result Downloader
A python tool to download result from csjmu official website


### Installation

1. Install Chrome Browser (Linux)
   [Install Chrome Browser Windows](https://www.google.com/intl/en/chrome/?standalone=1)
```
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i google-chrome-stable_current_amd64.deb
```



2. Install Python Packages
```
pip install selenium webdriver-manager
```

3. Run Program
```
python main.py
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


