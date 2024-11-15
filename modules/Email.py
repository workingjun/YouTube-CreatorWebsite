import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailManager:
    def SendEmail(self, sender_email, sender_password, recipient_email, subject, body):
        # Gmail SMTP 서버 설정
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587

        # 이메일 메시지 설정
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        try:
            # SMTP 서버에 연결
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  # TLS 암호화 시작
            server.login(sender_email, sender_password)  # 로그인
            server.send_message(msg)  # 이메일 보내기
            print("이메일이 성공적으로 발송되었습니다.")
        except Exception as e:
            print(f"이메일 발송 중 오류 발생: {e}")
        finally:
            server.quit()  # 서버 연결 종료