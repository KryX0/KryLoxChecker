# KryLox Checker

A Selenium-based tool to check Roblox account credentials from a combolist and categorize them into successful logins, failed logins, and accounts requiring verification.

## Features

- Automated login attempts using Firefox WebDriver
- Saves results to separate text files:
  - `successful_logins.txt`: Working credentials
  - `failed_logins.txt`: Invalid credentials or errors
  - `needs_verification.txt`: Accounts requiring manual verification
- Handles cookie consent popup
- Basic error handling for timeouts and invalid formats

## Prerequisites

- Python 3.x
- Firefox browser installed
- GeckoDriver (Firefox WebDriver) installed and in same folder as the code 

## Installation

Clone the repository:
```bash
git clone https://github.com/KryX0/KryLoxChecker.git
cd roblox-account-checker
```

Install required packages:
```bash
pip install -r requirements.txt
```
Or
```bash
pip install selenium colorama
```


## Usage

Prepare a combolist file (e.g., `combo.txt`) with credentials in the format:
```
username1:password1
username2:password2
```

Run the script:
```bash
python KryLoxChecker.py
```

Enter the name of your combolist file (without .txt extension) when prompted.


## Notes

- Important: Disable VPN/Proxy. 
- Ensure your Firefox browser is up to date for optimal performance.
 
## Example Output

```
[*] Connecting...
[*] Connected!

[NOTICE] Disable VPN/Proxy to potentially bypass verification challenges
[REMINDER] Ensure your Firefox browser is up to date for best performance

Combolist name: combo
[*] Results will be saved to 'successful_logins.txt', 'failed_logins.txt', and 'needs_verification.txt'
[!] GOOD: user1:pass1
[!] BAD: user2:pass2
[!] VERIFICATION REQUIRED: user3:pass3

[*] Done!
[*] Successful logins saved to: successful_logins.txt
[*] Failed logins saved to: failed_logins.txt
[*] Accounts needing verification saved to: needs_verification.txt
```

## Credits

- Forked from: XenonChecker

## Disclaimer

This tool is for educational purposes only. Use it responsibly and with permission. The author is not responsible for any misuse or damage caused by this tool.

## License

MIT License (LICENSE)
