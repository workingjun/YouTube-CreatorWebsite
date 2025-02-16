import os, logging
from datetime import datetime

def read_logs(filename, encoding="utf-8", num_lines=None) -> str:
    try:
        with open(filename, 'r', encoding=encoding) as log_file:
            if num_lines is None:
                return log_file.read()  # 전체 읽기
            else:
                # 마지막 num_lines만 읽기
                return ''.join(log_file.readlines()[-num_lines:])
    except FileNotFoundError:
        return f"Log file '{filename}' not found."
    except Exception as e:
        return f"Error reading log file: {e}"
        
class CustomFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, style='%', validate=True):
        if not fmt:
            #fmt = "%(asctime)s - %(levelname)s - %(funcName)s - %(message)s"
            fmt = "%(asctime)s - %(levelname)s - %(relpath)s:%(lineno)d - %(funcName)s - %(message)s"
        super().__init__(fmt, datefmt, style, validate)  # 부모 클래스의 __init__ 호출

    def format(self, record):
        try:
            record.relpath = os.path.relpath(record.pathname)
        except ValueError:  # 경로가 잘못된 경우 대비
            record.relpath = record.pathname
        return super().format(record)
    
    def formatTime(self, record, datefmt=None):
        # 원하는 형식을 명시
        datefmt = datefmt or '%Y-%m-%d %H:%M:%S'  # Default: YYYY-MM-DD HH:MM:SS,ms
        ct = self.converter(record.created)  # 기본 시간 변환기 사용 (localtime)
        return datetime.fromtimestamp(record.created).strftime(datefmt)

class BaseFileHandler(logging.Handler):
    def __init__(self, filename, mode='a', encoding='utf-8'):
        if mode not in ('a', 'w', 'x'):
            raise ValueError("Invalid mode: Choose 'a', 'w', or 'x'")
        directory = os.path.dirname(filename)
        if directory:  # 디렉토리가 비어 있지 않은 경우
            os.makedirs(directory, exist_ok=True)

        super().__init__()
        self.filename = filename
        self.file = open(filename, mode=mode, encoding=encoding, newline='')

    def close(self):
        if not self.file.closed:
            self.file.close()
        super().close()

class FileLoggingHandler(BaseFileHandler):
    def __init__(self, filename, mode='a', encoding='utf-8'):
        super().__init__(filename, mode, encoding)

    def emit(self, record):
        try:
            formatted_message = self.formatter.format(record)  # 포맷된 메시지
            self.file.write(formatted_message + "\n")
            self.file.flush()  # 파일에 즉시 기록
        except Exception:
            self.handleError(record)

class CustomLogging(logging.Logger):
    def __init__(self, name):
        super().__init__(name)
        self.setLevel(logging.DEBUG)

    def addHandler(self, filename, fmt=None, mode='a', encoding='utf-8'):
        for handler in self.handlers:
            if isinstance(handler, FileLoggingHandler) and handler.filename == filename:
                return  # 이미 동일한 핸들러가 추가된 경우 무시
        handler = FileLoggingHandler(filename, mode, encoding)
        handler.setFormatter(CustomFormatter(fmt))
        super().addHandler(handler)

class GetLogger:
    _instance = None  # 하나의 전역 로거 유지

    def __new__(cls, logger_name="app.log", logger_option="GlobalLogger"):
        if cls._instance is None:
            logger = CustomLogging(logger_option)  # 하나의 글로벌 로거 생성

            if not any(isinstance(h, logging.FileHandler) for h in logger.handlers):
                logger.addHandler(logger_name)

            cls._instance = logger  # 인스턴스 저장

        return cls._instance  # 동일한 로거 반환
    
if __name__=="__main__":
    # 로거 설정
    logger = CustomLogging("DualLogger")
    logger.addHandler("everytime_autoLike.log")

    # 로깅 테스트
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
