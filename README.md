# CSJMU Result Downloader
A python tool to download result from csjmu official website. It now supports AKTU Result fetching.

### Features
* Automated Result Download: Fetch results for multiple students in bulk.
* Flexible Input: Accepts input in various formats including Excel Sheet and JSON.
* Date Handling: Converts and formats dates for easy reference.
* Web Scraping: Utilizes Selenium for navigating and extracting data from the official result page.

### Prerequisites
Before you begin, ensure you have met the following requirements:

* Python 3.x
* Chrome Browser


### ⚙ Installation

1. Install Chrome Browser (Linux)
   [Install Chrome Browser Windows](https://www.google.com/intl/en/chrome/?standalone=1)
```
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i google-chrome-stable_current_amd64.deb
```

2. Clone Respository
```
git clone https://github.com/SanjaySRocks/csjmu-result-downloader.git
```

2. Install dependencies
```
pip install selenium webdriver-manager pandas
```

3. Run script
```
python main.py
```

### 🤖 Usage:

1. Get student result by name, rollno, dob

```
result = CSJMUResult()
result.process_student("MANASVI MISHRA", 22015003575, "05/27/2006")
result.close()
```

2. Get all result by providing a list of students (required students excel sheet)

Excel Sheet :- <br>
Column name should be same as (Roll Number, Full Name, Date of Birth) in order to work

![img](https://i.imgur.com/EAOitxX.png)

```
result = CSJMUResult()
result.read_excel_sheet(filename="1BCA-A.xlsx")
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


### Contributing
If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (**git checkout -b feature-branch**).
3. Make your changes.
4. Commit your changes (**git commit -am 'Add new feature'**).
5. Push to the branch (**git push origin feature-branch**).
6. Open a Pull Request.

### License
This project is licensed under the MIT License - see the LICENSE file for details.

### Contact
For any questions or issues, contact me

