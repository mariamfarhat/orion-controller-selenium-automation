# Orion Controller Selenium Automation

A Python-based automation tool that uses Selenium WebDriver to automate login and system time/date configuration for Orion/SNMP controllers. The tool reads configuration data from an Excel file and performs batch operations across multiple controllers.

## Features

- **Automated Login**: Securely logs into Orion/SNMP controllers using credentials from Excel input
- **Time/Date Configuration**: Updates system time and date settings, including NTP server configuration
- **Batch Processing**: Processes multiple controllers from a single Excel file
- **Headless Operation**: Runs in headless Chrome mode for server environments
- **Error Handling**: Includes fallback mechanisms for read-only fields and exception handling

## Prerequisites

- Python 3.8 or higher
- Google Chrome browser
- Excel file with controller details (see Data Format section)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/orion-controller-selenium-automation.git
   cd orion-controller-selenium-automation
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Ensure Chrome is installed on your system.

## Usage

1. Prepare your Excel file in the `data/` directory with controller information (see Data Format below).

2. Run the automation script:
   ```bash
   cd src
   python main.py
   ```

The script will process each row in the Excel file, logging into the respective controller and updating the time/date configuration.

## Data Format

The Excel file (`data/test_snmp.xlsx`) should contain the following columns:

| Column    | Description                  | Example          |
|-----------|------------------------------|------------------|
| host      | Controller IP address or hostname | 192.168.1.100   |
| port      | Controller web interface port | 80              |
| username  | Login username               | admin            |
| password  | Login password               | password123      |

Example Excel structure:
```
host          | port | username | password
--------------|------|----------|----------
192.168.1.100 | 80   | admin    | pass123
192.168.1.101 | 80   | admin    | pass456
```

## Configuration

The script currently sets the NTP server to `192.168.1.1`. To modify this value, edit the `value_to_set` variable in `src/main.py`.

## Dependencies

- Selenium: Web automation
- Pandas: Excel file processing
- WebDriver Manager: Automatic ChromeDriver management
- OpenPyXL: Excel file support

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Security Recommendation

- Hash or encrypt passwords
- Use environment variables
- Avoid storing credentials in plain Excel files

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is provided as-is for automation purposes. Ensure you have proper authorization before running automation against network devices. Test in a development environment first.
