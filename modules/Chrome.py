import chromedriver_autoinstaller
from selenium import webdriver
import os
import subprocess

class ChromeManager:
    chrome_path_case1 = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    chrome_path_case2 = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
    current_dir = os.getcwd()
    user_data_dir = os.path.join(current_dir, 'chrometemp')
    OPTIONS = ["--remote-debugging-port=9221", f'--user-data-dir="{user_data_dir}"', "--no-first-run",
               "--no-default-browser-check", "--disable-extensions", "--disable-plugins", 
               "--disable-infobars", "--headless"]

    def __init__(self, url):
        self.chrome_process = None
        self.browser = None
        self.url = url

    def process_Chrome(self):
        # Chrome 실행 설정
        chrome_command = f'"{self.chrome_path_case1}" ' + " ".join(self.OPTIONS)
        try:
            self.chrome_process = subprocess.Popen(chrome_command)
        except FileNotFoundError:
            chrome_command = f'"{self.chrome_path_case2}" ' + " ".join(self.OPTIONS)
            self.chrome_process = subprocess.Popen(chrome_command)
        
        # 브라우저 설정 및 연결
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9221")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        
        chromedriver_autoinstaller.install()
        self.browser = webdriver.Chrome(options=chrome_options)
        self.browser.maximize_window()
        self.browser.get(self.url)
        self.browser.implicitly_wait(3)

    def terminate_chrome_process(self):
        if self.chrome_process:
            self.chrome_process.terminate()