from selenium.webdriver.common.by import By
from modules.Chrome import ChromeManager

class NewsManager:
    def __init__(self, Chrome: ChromeManager):
        self.Chrome = Chrome
        self.browser = self.Chrome.browser
        self.result = self.create_email_content()
        
    def create_email_content(self):
        xpaths = [
            "//article[@class='IBr9hb']",
            "//article[@class='UwIKyb']",
            "//article[@class='IFHyqb']"
        ]
        num = 0
        email_content = """
        <html>
        <head><style>
            body { font-family: Arial, sans-serif; }
            .headline { margin-bottom: 20px; }
            .separator { border-bottom: 1px solid #ccc; margin: 20px 0; }
            .headline-title { font-weight: bold; font-size: 16px; }
            .headline-content { margin-top: 10px; font-size: 14px; }
            a { color: #1a0dab; text-decoration: none; }
        </style></head>
        <body>
        <h1>News Headlines</h1>
        <hr>
        """
        for xpath in xpaths:
            try:
                articles = self.browser.find_elements(By.XPATH, xpath)
            except:
                continue
            else:
                for article in articles:
                    num += 1
                    try:
                        link_elem = article.find_element(By.CLASS_NAME, "WwrzSb")
                        link = link_elem.get_attribute("href")
                        short_link = f'<a href="{link}" target="_blank">클릭하여 기사 열기</a>'
                    except:
                        link = "No link available"
                        short_link = link
                    
                    headline_text = article.text
                    try:
                        title = headline_text.splitlines()[1]
                        time = headline_text.splitlines()[2]
                        newpaper = headline_text.splitlines()[0]
                        if "작성자" in time:
                            title = headline_text.splitlines()[0]
                            time = headline_text.splitlines()[1]
                            newpaper = headline_text.splitlines()[2].replace("작성자: ", "")
                    except IndexError:
                        title = headline_text.splitlines()[0]
                        time = headline_text.splitlines()[1] if len(headline_text.splitlines()) > 1 else "시간 정보 없음"
                        newpaper = "정보없음"
                    
                    email_content += f"""
                    <div class="headline">
                        <p class="headline-title">Headline {num} 📌 {title}</p>
                        <p class="headline-content">📰 신문사: {newpaper}</p>
                        <p class="headline-content">⏰ 업데이트: {time}</p>
                        <p class="headline-content">🔗 링크: {short_link}</p>
                    </div>
                    <div class="separator"></div>
                    """
        email_content += """
        </body>
        </html>
        """
        return email_content
            
    