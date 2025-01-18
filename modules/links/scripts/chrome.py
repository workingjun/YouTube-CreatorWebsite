import os
import subprocess, shlex
from selenium import webdriver
import chromedriver_autoinstaller
from selenium_stealth import stealth

class ChromeDriverManager:
    def __init__(self, debug_flag, close_flag: bool = True, headless_flag: bool = False):
        self.close_flag = close_flag
        self.headless_flag = headless_flag
        self.browser = None
        self.__chrome_process = None
        if debug_flag:
            self._start_chrome_process()
        self.browser = self._initialize_webdriver()
        self._apply_stealth()
        
    def __enter__(self):
        """Returns the WebDriver instance when entering the context."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Ensures that resources are cleaned up on exiting the context."""
        if self.close_flag:
            self._terminate_process()

    def _start_chrome_process(self):
        if not os.path.exists("C:/chrometmp"):
            os.mkdir("C:/chrometmp")
        try:
            chrome_path = rf"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
            chrome_command = rf'{chrome_path} --remote-debugging-port=9222 --no-first-run'
            print(f"[INFO] Starting Chrome subprocess with command: {chrome_command}")
            self.__chrome_process = subprocess.Popen(shlex.split(chrome_command))

        except FileNotFoundError:
            chrome_path = rf"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
            chrome_command = rf'{chrome_path} --remote-debugging-port=9222 --no-first-run'
            print(f"[INFO] Starting Chrome subprocess with command: {chrome_command}")
            self.__chrome_process = subprocess.Popen(shlex.split(chrome_command))

        except Exception as e:
            print(f"[ERROR] Failed to start Chrome subprocess: {e}")
            raise RuntimeError("[ERROR] Chrome process failed to start")

    def _initialize_webdriver(self) -> webdriver.Chrome:
        print("[INFO] Initializing WebDriver...")
        chromedriver_autoinstaller.install()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        if self.__chrome_process is not None:
            chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

        # 헤드리스 모드 적용
        if self.headless_flag:
            print("[INFO] Enabling headless mode...")
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")

        try:
            return webdriver.Chrome(options=chrome_options)
            
        except Exception as e:
            print(f"[ERROR] Failed to initialize WebDriver: {e}")
            self._terminate_process()
            raise RuntimeError("WebDriver initialization failed.")
    
    def _apply_stealth(self):
        try:
            stealth(self.browser,
                    languages=["en-US", "en"],
                    vendor="Google Inc.",
                    platform="Win32",
                    webgl_vendor="Intel Inc.",
                    renderer="Intel Iris OpenGL Engine",
                    fix_hairline=True)
            print("[INFO] Stealth settings successfully applied.")
        except Exception as e:
            print(f"[ERROR] Failed to apply stealth settings: {e}")
            raise RuntimeError("Failed to apply stealth settings.")
        
    def _terminate_process(self):
        if self.browser:
            try:
                self.browser.quit()
            except Exception as e:
                print(f"[WARNING] Failed to quit WebDriver: {e}")
        if self.__chrome_process:
            try:
                self.__chrome_process.terminate()
            except Exception as e:
                print(f"[WARNING] Failed to terminate Chrome process: {e}")

    def get_url(self, url: str, maximize_flag: bool = False, wait: int = 3):
        browser = self.get_browser()
        if maximize_flag:
            browser.maximize_window()
        print(f"[INFO] Navigating to URL: {url}")
        browser.get(url)
        browser.implicitly_wait(wait)

    def get_browser(self):
        if not self.browser:
            raise RuntimeError("[ERROR] Browser is not initialized.")
        return self.browser
    
