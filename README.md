Orion Controller Selenium Automation

This project is a Python Selenium automation script that logs into an Orion/SNMP web controller, navigates to the system time/date configuration page, and reads or updates configuration values based on whether the field is editable or read-only.

The script reads multiple device credentials from an Excel file, making it suitable for automating configuration across multiple telecom sites or controllers.

🚀 Features

- Reads host, port, username, and password from an Excel file

- Automates login to Orion/SNMP web controller

- Navigates to system Time & Date configuration

- Detects whether a field is:

    Editable (<input>)

    Read-only (<div>)

- Updates configuration values when editable

- Works with headless or visible Chrome

- Handles Selenium exceptions gracefully

🧰 Technologies Used

- Python 3

- Selenium WebDriver

- Pandas

- ChromeDriver Manager

- Excel (.xlsx) input


📂 Project Structure
.
├── data/
│   └── test_snmp.xlsx
├── main.py
├── requirements.txt
└── README.md

📊 Excel Input Format

The Excel file data/test_snmp.xlsx must contain the following columns:

host	port	username	password
192.168.1.10	8080	admin	admin123

Each row represents a controller to automate.

⚙️ Installation
1️⃣ Clone the repository
git clone https://github.com/yourusername/orion-controller-selenium-automation.git
cd orion-controller-selenium-automation

2️⃣ Install dependencies
pip install -r requirements.txt

📦 requirements.txt
selenium
pandas
webdriver-manager
openpyxl
requests
beautifulsoup4

▶️ Usage

Run the script:

python main.py


What happens:

Reads controller details from Excel

Opens the login page

Logs in automatically

Navigates to:

/controller/configuration/system/timedate


Reads or updates the configuration field

Applies and reloads settings if editable

🧠 Logic Handling

- Editable Field

- Reads value from <input>
 
- Updates value

- Clicks Accept and Reload

- Read-Only Field

- Reads value from <div>

- Logs the value only

This makes the script robust against UI differences across firmware versions.

⚠️ Notes & Warnings

- Make sure Chrome is installed

- Do not expose real credentials in public repos

- Some controllers may block automation without delays

- Adjust time.sleep() values if pages load slowly

🔐 Security Recommendation

For production use:

- Hash or encrypt passwords

- Use environment variables

- Avoid storing credentials in plain Excel files
