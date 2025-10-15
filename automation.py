# --- 경고: 아래 코드는 테스트 전용이며, 절대 이대로 저장소에 남겨두면 안 됩니다 ---

import smtplib
import os
from email.mime.text import MIMEText
import ssl

# --- 여기에 직접 ID와 앱 비밀번호를 입력합니다 ---
SMTP_USER = "wjsdbfla1208@naver.com"  # 👈 여기에 본인 네이버 이메일 주소 전체를 입력하세요.
SMTP_PASSWORD = "965JT2KWQUR2"      # 👈 여기에 방금 발급받은 12자리 앱 비밀번호를 입력하세요.
# ----------------------------------------------------

# 나머지 정보는 기존과 동일하게 GitHub Secrets에서 가져옵니다.
RECIPIENT_EMAIL = os.environ.get('RECIPIENT_EMAIL')
LOCATION = os.environ.get('LOCATION')
YEAR = os.environ.get('YEAR')
JOBS = os.environ.get('JOBS')

# ... (이하 코드는 이전과 동일) ...

print("--- [테스트 모드] 코드에 직접 입력된 값으로 로그인 시도 ---")
print(f"SMTP_USER: {SMTP_USER[:5]}... (직접 입력됨)") # 보안을 위해 일부만 표시

if not all([SMTP_USER, SMTP_PASSWORD, RECIPIENT_EMAIL]):
    print("오류: 코드에 직접 입력한 값 또는 수신자 이메일이 설정되지 않았습니다.")
    exit(1)

try:
    msg = MIMEText(f"이 메일은 코드에 ID/비밀번호를 직접 입력하는 최종 테스트 과정에서 발송되었습니다.", 'html', 'utf-8')
    msg['Subject'] = f"[{LOCATION}] 최종 발송 테스트"
    msg['From'] = SMTP_USER
    msg['To'] = RECIPIENT_EMAIL

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.naver.com", 465, context=context) as smtp:
        smtp.login(SMTP_USER, SMTP_PASSWORD)
        smtp.send_message(msg)
        print("🎉🎉🎉 [성공] 이메일 발송에 성공했습니다! 🎉🎉🎉")

except Exception as e:
    print("❌❌❌ [실패] 여전히 이메일 발송에 실패했습니다. ❌❌❌")
    print(f"   자세한 오류 내용: {e}")
    exit(1)
