import smtplib
import os
from email.mime.text import MIMEText
import ssl

# --- 설정 값 불러오기 ---
SMTP_SERVER = "smtp.naver.com"
SMTP_PORT = 465  # SSL 보안 연결 포트
SMTP_USER = os.environ.get('SMTP_USER')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')

RECIPIENT_EMAIL = os.environ.get('RECIPIENT_EMAIL')
LOCATION = os.environ.get('LOCATION')
YEAR = os.environ.get('YEAR')
JOBS = os.environ.get('JOBS')

# --- 필수 값 검증 ---
print("--- 환경 변수 확인 시작 ---")
print(f"SMTP_USER: {'설정됨' if SMTP_USER else '***설정 안됨***'}")
print(f"SMTP_PASSWORD: {'설정됨' if SMTP_PASSWORD else '***설정 안됨***'}")
print(f"RECIPIENT_EMAIL: {'설정됨' if RECIPIENT_EMAIL else '***설정 안됨***'}")
print("--------------------------")

if not all([SMTP_USER, SMTP_PASSWORD, RECIPIENT_EMAIL]):
    print("오류: 필수 Secret(SMTP_USER, SMTP_PASSWORD, RECIPIENT_EMAIL) 중 하나 이상이 설정되지 않았습니다.")
    exit(1)

# --- 이메일 메시지 생성 ---
try:
    subject = f"[{LOCATION}] {YEAR}년 {JOBS} 관련 정보입니다."
    body = f"요청하신 {YEAR}년 {LOCATION} 지역의 {JOBS} 관련 정보를 보내드립니다.\n\n이 메일은 GitHub Actions를 통해 자동으로 발송되었습니다."
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = SMTP_USER
    msg['To'] = RECIPIENT_EMAIL

except Exception as e:
    print(f"오류: 이메일 메시지 생성 중 문제가 발생했습니다: {e}")
    exit(1)

# --- 이메일 발송 ---
print("Naver SMTP 서버에 보안 연결(SSL)을 시도합니다...")
try:
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as smtp:
        print("서버 연결 성공. 로그인을 시도합니다...")
        smtp.login(SMTP_USER, SMTP_PASSWORD)
        print("로그인 성공. 이메일을 발송합니다...")
        smtp.send_message(msg)
        print(f"🎉 성공! '{RECIPIENT_EMAIL}' 주소로 이메일을 성공적으로 발송했습니다.")

except smtplib.SMTPAuthenticationError:
    print("❌ 오류: SMTP 인증 실패. 'Username and Password not accepted'.")
    print("   원인: 1) ID 또는 앱 비밀번호가 정확하지 않거나, 2) Naver 보안 설정(해외 로그인 차단 등)에 의해 거부되었습니다.")
    exit(1)
except Exception as e:
    print(f"❌ 오류: 이메일 발송 중 예상치 못한 문제가 발생했습니다: {e}")
    exit(1)
