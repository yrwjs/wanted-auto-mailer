import smtplib
import os
from email.mime.text import MIMEText
import ssl

# --- 설정 값 불러오기 ---
# GitHub Secrets와 워크플로우 환경 변수에서 설정 값을 읽어옵니다.
SMTP_SERVER = "smtp.naver.com"
SMTP_PORT = 465 # SSL 연결을 위한 표준 포트
SMTP_USER = os.environ.get('SMTP_USER')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')

RECIPIENT_EMAIL = os.environ.get('RECIPIENT_EMAIL')
LOCATION = os.environ.get('LOCATION')
YEAR = os.environ.get('YEAR')
JOBS = os.environ.get('JOBS')

# --- 1. 필수 값 검증 ---
print("--- 환경 변수 확인 시작 ---")
print(f"SMTP_USER: {'설정됨' if SMTP_USER else '***설정 안됨***'}")
print(f"SMTP_PASSWORD: {'설정됨' if SMTP_PASSWORD else '***설정 안됨***'}")
print(f"RECIPIENT_EMAIL: {'설정됨' if RECIPIENT_EMAIL else '***설정 안됨***'}")
print("--------------------------")

if not all([SMTP_USER, SMTP_PASSWORD, RECIPIENT_EMAIL]):
    print("오류: SMTP 사용자, 비밀번호, 또는 수신자 이메일이 설정되지 않았습니다.")
    exit(1)

# --- 2. 이메일 메시지 생성 ---
try:
    subject = f"[{LOCATION}] {YEAR}년 {JOBS} 관련 정보입니다."
    body = f"""
    안녕하세요.

    요청하신 {YEAR}년 {LOCATION} 지역의 {JOBS} 관련 정보를 보내드립니다.

    이 메일은 GitHub Actions를 통해 자동으로 발송되었습니다.

    감사합니다.
    """

    msg = MIMEText(body, 'html', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = SMTP_USER
    msg['To'] = RECIPIENT_EMAIL

except Exception as e:
    print(f"오류: 이메일 메시지 생성 중 문제가 발생했습니다: {e}")
    exit(1)

# --- 3. 이메일 발송 ---
print("SMTP 서버에 연결을 시도합니다...")
try:
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as smtp:
        print("서버에 연결되었습니다. 로그인을 시도합니다...")
        smtp.login(SMTP_USER, SMTP_PASSWORD)
        print("로그인 성공. 이메일을 발송합니다...")
        smtp.send_message(msg)
        print(f"성공적으로 이메일을 발송했습니다: {RECIPIENT_EMAIL}")

except smtplib.SMTPAuthenticationError:
    print("오류: SMTP 인증 실패. 'Username and Password not accepted'.")
    print("원인: ID 또는 앱 비밀번호가 정확하지 않습니다. GitHub Secrets 값을 다시 확인하세요.")
    exit(1)
except Exception as e:
    print(f"오류: 이메일 발송 중 예상치 못한 문제가 발생했습니다: {e}")
    exit(1)
