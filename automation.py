import smtplib
import os
from email.mime.text import MIMEText

# GitHub Secrets와 워크플로우 환경 변수에서 설정 값 불러오기
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = os.environ.get('SMTP_USER')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')

recipient_email = os.environ.get('RECIPIENT_EMAIL')
location = os.environ.get('LOCATION')
year = os.environ.get('YEAR')
jobs = os.environ.get('JOBS')

# 필수 값들이 모두 있는지 확인
if not all([SMTP_USER, SMTP_PASSWORD, recipient_email, location, year, jobs]):
    print("오류: 필요한 환경 변수 중 일부가 설정되지 않았습니다.")
    exit(1)

# 이메일 제목 및 본문 생성
subject = f"[{location}] {year}년 {jobs} 관련 정보입니다."
body = f"""
안녕하세요.

요청하신 {year}년 {location} 지역의 {jobs} 관련 정보를 보내드립니다.

이 메일은 GitHub Actions를 통해 자동으로 발송되었습니다.

감사합니다.
"""

# 터미널에 로그를 출력하여 Actions 탭에서 확인할 수 있도록 함
print(f"발신자: {SMTP_USER}")
print(f"수신자: {recipient_email}")
print(f"제목: {subject}")

# 이메일 발송
try:
    smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    smtp.starttls()
    smtp.login(SMTP_USER, SMTP_PASSWORD)

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SMTP_USER
    msg['To'] = recipient_email

    smtp.sendmail(SMTP_USER, recipient_email, msg.as_string())
    smtp.quit()
    print(f"성공적으로 이메일을 발송했습니다: {recipient_email}")

except Exception as e:
    print(f"이메일 발송 중 오류가 발생했습니다: {e}")
    exit(1)
