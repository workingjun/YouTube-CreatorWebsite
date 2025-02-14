import os, socket, shlex
from typing import Optional
from subprocess import Popen
import chromedriver_autoinstaller
from selenium_stealth import stealth
from selenium.webdriver import Chrome, ChromeOptions

# Chrome 실행 경로 목록
CHROME_PATHS = [
    r"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
    r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
]

DEFAULT_OPTIONS = [
    "--disable-gpu",
    "--disable-dev-shm-usage",
    "--no-first-run",
    "--log-level=3"
]

DEFAULT_OPTIONS_STR = "--disable-gpu --disable-dev-shm-usage --no-first-run --log-level=3"

def find_available_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))  # OS가 사용 가능한 포트를 자동 할당
        return s.getsockname()[1]

def find_chrome_path() -> Optional[str]:
    """CHROME_PATHS 중 존재하는 실행 파일 경로를 반환"""
    return next((path for path in CHROME_PATHS if os.path.exists(path)), None)

class ChromeSubprocessManager:
    def __init__(self):
        self.process: Optional[Popen] = None

    def start_process(self, args, headless: bool, available_port: int):
        print("Starting Chrome subprocess...")

        if args is None:
            args = DEFAULT_OPTIONS
        elif isinstance(args, str):
            args = shlex.split(args)
        elif not isinstance(args, list):
            raise TypeError("args must be either a string or a list of strings")

        chrome_path = find_chrome_path()
        if chrome_path is None:
            print("Chrome executable not found.")
            raise FileNotFoundError("Chrome executable not found.")

        chrome_command = [chrome_path] + args
        chrome_command.append(f"--remote-debugging-port={available_port}")
        if headless:
            chrome_command.append("--headless=new")
        try:
            self.process = Popen(chrome_command)
            print("Chrome subprocess started.")
        except Exception as e:
            print("Failed to start Chrome subprocess: %s", e)
            raise

    def terminate_process(self) -> bool:
        if not self.process:
            return False
        try:
            self.process.terminate()
            print("Chrome subprocess terminated.")
            self.process = None  # 프로세스 정리
            return True
        except Exception as e:
            print("Failed to terminate Chrome subprocess: %s", e)
            return False

class WebDriverManager:
    def __init__(self):
        self.browser: Optional["Chrome"] = None

    def start_driver(self, available_port: int):
        chromedriver_autoinstaller.install()
        options = ChromeOptions()
        options.add_experimental_option("debuggerAddress", f"127.0.0.1:{available_port}")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36")

        try:
            self.browser = Chrome(options=options)
            print("WebDriver initialized.")
        except Exception as e:
            print("Failed to start WebDriver: %s", e)
            raise

    def navigate_to(self, url: str, maximize: bool = True, wait: int = 3):
        if not self.browser:
            print("WebDriver is not initialized.")
            return

        try:
            print("Navigating to %s...", url)
            self.browser.get(url)

            if maximize:
                self.browser.maximize_window()
            self.browser.implicitly_wait(wait)
        except Exception as e:
            print("Failed to navigate to %s: %s", url, e)

    def apply_stealth(self):
        if not self.browser:
            return
        try:
            stealth(
                self.browser,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True
            )
            
            print("Stealth settings applied.")
        except Exception as e:
            print("Failed to apply stealth settings: %s", e)

    def quit_driver(self):
        if self.browser:
            self.browser.quit()
            print("WebDriver terminated.")
            self.browser = None  # WebDriver 정리

class ChromeDriverManager:
    def __init__(self):
        self.subprocess_manager: ChromeSubprocessManager = ChromeSubprocessManager()
        self.webdriver_manager: WebDriverManager = WebDriverManager()
        self.is_running: bool = False

    def __enter__(self) -> "ChromeDriverManager":
        """ with 문에서 사용할 때 자동 실행 """
        return self  # 객체 자체를 반환

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        """ with 문 종료 시 자동 실행 """
        if exc_type is not None:
            print("Exception occurred in ChromeDriverManager: %s", exc_value)

        self.stop()  # 안전한 종료 처리
        return False  # 예외를 다시 발생시켜 상위 코드에서 처리할 수 있도록 함.

    @property
    def browser(self) -> Optional["Chrome"]:
        if not self.webdriver_manager.browser:
            print("Browser is not initialized")
        return self.webdriver_manager.browser

    @browser.setter
    def browser(self, value):
        self.webdriver_manager.browser = value

    def start(self, url, headless: bool, maximize: bool = True, wait: int = 3):
        if self.is_running:
            print("ChromeDriverManager is already running.")
            return

        try:
            available_port = find_available_port()
            self.subprocess_manager.start_process(DEFAULT_OPTIONS, headless, available_port)
            self.webdriver_manager.start_driver(available_port)
            self.webdriver_manager.navigate_to(url, maximize, wait)
            self.webdriver_manager.apply_stealth()
            self.is_running = True
        except Exception as e:
            print("Failed to start ChromeDriverManager: %s", e)
            self.stop()  # 예외 발생 시 안전하게 정리
            raise

    def stop(self):
        """ Chrome 및 WebDriver 안전 종료 """
        if self.subprocess_manager.process:
            self.subprocess_manager.terminate_process()

        self.is_running = False
        print("ChromeDriverManager stopped.")

if __name__ == "__main__":
    try:
        with ChromeDriverManager() as manager:
            manager.start(headless=False, url="https://everytime.kr/")
            input("Press Enter to stop...")  # 테스트용

    except KeyboardInterrupt:
        print("User interrupted execution. Stopping ChromeDriverManager.")
    except Exception as e:
        print("Unexpected error: %s", e)






