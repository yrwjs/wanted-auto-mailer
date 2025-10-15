# local_test.py

import smtplib
import ssl
from email.mime.text import MIMEText

# --- 1. 터미널에서 직접 로그인 정보 입력받기 ---
smtp_user = input("네이버 이메일 주소 전체를 입력하세요: ")
smtp_password = input("네이버 앱 비밀번호 (12자리)를 입력하세요: ")
recipient_email = input("메일을 받을 주소를 입력하세요: ")

# --- 2. 이메일 메시지 생성 ---
subject = "[로컬 PC 테스트] 자동 메일 발송"
body = "이 메일은 개인 PC에서 직접 파이썬 코드를 실행하여 보낸 테스트 메일입니다."
msg = MIMEText(body, 'html', 'utf-8')
msg['Subject'] = subject
msg['From'] = smtp_user
msg['To'] = recipient_email

# --- 3. 이메일 발송 ---
print("\nNaver SMTP 서버에 연결을 시도합니다...")
try:
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.naver.com", 465, context=context) as smtp:
        print("서버 연결 성공. 로그인을 시도합니다...")
        smtp.login(smtp_user, smtp_password)
        print("로그인 성공! 이메일을 발송합니다...")
        smtp.send_message(msg)
        print(f"\n🎉 성공! '{recipient_email}' 주소로 메일을 성공적으로 보냈습니다.")

except Exception as e:
    print(f"\n❌ 실패! 이메일 발송 중 오류가 발생했습니다.")
    print(f"오류 내용: {e}")
