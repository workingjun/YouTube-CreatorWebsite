from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

class ChromeDriverPythonAnywhere:
    
    CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"

    def __init__(self, close_flag: bool = True, headless_flag: bool = False):
        self.close_flag = close_flag
        self.headless_flag = headless_flag
        self.browser = None
        self.browser = self._initialize_webdriver()
        self._apply_stealth()
        
    def __enter__(self):
        """Returns the WebDriver instance when entering the context."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Ensures that resources are cleaned up on exiting the context."""
        if self.close_flag:
            self._terminate_process()

    def _initialize_webdriver(self) -> webdriver.Chrome:
        print("[INFO] Initializing WebDriver...")
        chrome_options = Options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        # 헤드리스 모드 적용
        if self.headless_flag:
            print("[INFO] Enabling headless mode...")
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")

        try:
            # WebDriver 초기화
            service = Service(executable_path=self.CHROMEDRIVER_PATH)
            return webdriver.Chrome(service=service, options=chrome_options)
            
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
    
