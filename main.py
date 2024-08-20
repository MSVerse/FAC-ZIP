import zipfile
import itertools
import threading
import time
import string
import sys

def print_banner():
    banner = """
⠀⠀⠀⣠⠂⢀⣠⡴⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⢤⣄⠀⠐⣄⠀⠀⠀
⠀⢀⣾⠃⢰⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⡆⠸⣧⠀⠀
⢀⣾⡇⠀⠘⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⠁⠀⢹⣧⠀
⢸⣿⠀⠀⠀⢹⣷⣀⣤⣤⣀⣀⣠⣶⠂⠰⣦⡄⢀⣤⣤⣀⣀⣾⠇⠀⠀⠈⣿⡆
⣿⣿⠀⠀⠀⠀⠛⠛⢛⣛⣛⣿⣿⣿⣶⣾⣿⣿⣿⣛⣛⠛⠛⠛⠀⠀⠀⠀⣿⣷
⣿⣿⣀⣀⠀⠀⢀⣴⣿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⣀⣠⣿⣿
⠛⠻⠿⠿⣿⣿⠟⣫⣶⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣙⠿⣿⣿⠿⠿⠛⠋
⠀⠀⠀⠀⠀⣠⣾⠟⣯⣾⠟⣻⣿⣿⣿⣿⣿⣿⡟⠻⣿⣝⠿⣷⣌⠀⠀⠀⠀⠀
⠀⠀⢀⣤⡾⠛⠁⢸⣿⠇⠀⣿⣿⣿⣿⣿⣿⣿⣿⠀⢹⣿⠀⠈⠻⣷⣄⡀⠀⠀
⢸⣿⡿⠋⠀⠀⠀⢸⣿⠀⠀⢿⣿⣿⣿⣿⣿⣿⡟⠀⢸⣿⠆⠀⠀⠈⠻⣿⣿⡇
⢸⣿⡇⠀⠀⠀⠀⢸⣿⡀⠀⠘⣿⣿⣿⣿⣿⡿⠁⠀⢸⣿⠀⠀⠀⠀⠀⢸⣿⡇
⢸⣿⡇⠀⠀⠀⠀⢸⣿⡇⠀⠀⠈⢿⣿⣿⡿⠁⠀⠀⢸⣿⠀⠀⠀⠀⠀⣼⣿⠃
⠈⣿⣷⠀⠀⠀⠀⢸⣿⡇⠀⠀⠀⠈⢻⠟⠁⠀⠀⠀⣼⣿⡇⠀⠀⠀⠀⣿⣿⠀
⠀⢿⣿⡄⠀⠀⠀⢸⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⡇⠀⠀⠀⢰⣿⡟⠀
⠀⠈⣿⣷⠀⠀⠀⢸⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⠃⠀⠀⢀⣿⡿⠁⠀
⠀⠀⠈⠻⣧⡀⠀⠀⢻⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⡟⠀⠀⢀⣾⠟⠁⠀⠀
⠀⠀⠀⠀⠀⠁⠀⠀⠈⢿⣿⡆⠀⠀⠀⠀⠀⠀⣸⣿⡟⠀⠀⠀⠉⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⡄⠀⠀⠀⠀⣰⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠆⠀⠀⠐⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
              FAC-ZIP
    """
    print(banner)

class ZipBruteForcer:
    def __init__(self, zip_filename, max_len=4, num_threads=10, charset=None, wordlist=None):
        self.zip_filename = zip_filename
        self.max_len = max_len
        self.num_threads = num_threads
        self.charset = charset or string.ascii_letters + string.digits
        self.wordlist = wordlist
        self.found = False
        self.lock = threading.Lock()

    def attempt_password(self, password):
        try:
            with zipfile.ZipFile(self.zip_filename, 'r') as zf:
                zf.extractall(pwd=password.encode('utf-8'))
            return True
        except:
            return False

    def bruteforce(self, start_index, end_index):
        for i in range(start_index, end_index):
            if self.found:
                return
            password = ''.join(itertools.product(self.charset, repeat=i))
            if self.attempt_password(password):
                with self.lock:
                    self.found = True
                    print(f'[+] Password found: {password}')
                    sys.exit(0)

    def wordlist_attack(self):
        if not self.wordlist:
            print("[-] No wordlist provided.")
            return

        with open(self.wordlist, 'r') as file:
            for line in file:
                if self.found:
                    return
                password = line.strip()
                if self.attempt_password(password):
                    with self.lock:
                        self.found = True
                        print(f'[+] Password found: {password}')
                        sys.exit(0)

    def start(self):
        if self.wordlist:
            print("[*] Starting wordlist attack...")
            self.wordlist_attack()
        else:
            print("[*] Starting brute-force attack...")
            threads = []
            for i in range(1, self.max_len + 1):
                for j in range(self.num_threads):
                    start_index = int(j * (len(self.charset) ** i) / self.num_threads)
                    end_index = int((j + 1) * (len(self.charset) ** i) / self.num_threads)
                    t = threading.Thread(target=self.bruteforce, args=(start_index, end_index))
                    threads.append(t)
                    t.start()

            for t in threads:
                t.join()

        if not self.found:
            print("[-] Password not found.")

if __name__ == "__main__":
    print_banner()
    zip_filename = input("[*] Enter ZIP file path: ")
    mode = input("[*] Choose attack mode (1 for brute-force, 2 for wordlist): ")

    if mode == '1':
        max_len = int(input("[*] Enter maximum password length: "))
        num_threads = int(input("[*] Enter number of threads: "))
        charset = input("[*] Enter character set (leave blank for default): ") or None
        brute_forcer = ZipBruteForcer(zip_filename, max_len, num_threads, charset)
        brute_forcer.start()

    elif mode == '2':
        wordlist = input("[*] Enter wordlist file path: ")
        brute_forcer = ZipBruteForcer(zip_filename, wordlist=wordlist)
        brute_forcer.start()
    else:
        print("[-] Invalid mode selected.")
