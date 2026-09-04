import requests
import json
from datetime import datetime

# ============ 설정 영역 ============
TELEGRAM_BOT_TOKEN = "여기에_봇_토큰_입력"  # @BotFather 에서 발급
TELEGRAM_CHAT_ID = "여기에_채팅_ID_입력"    # 봇을 추가한 채널/그룹 ID

# 방송 상태 API 엔드포인트 (예시)
BROADCAST_STATUS_URL = "https://api.example.com/broadcast/status"
# ==================================

def send_telegram_message(message):
    """텔레그램으로 메시지를 전송합니다"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"  # HTML 형식 사용 (볼드, 이탤릭 등)
    }
    
    response = requests.post(url, json=data)
    return response.json()

def check_broadcast_status():
    """방송 상태를 확인합니다"""
    response = requests.get(BROADCAST_STATUS_URL)
    return response.json()

def notify_live_start(channel_name):
    """방송 시작 알림"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    message = f"""
🔴 <b>방송이 시작되었습니다!</b>

📺 채널: {channel_name}
⏰ 시간: {now}

지금 바로 시청하세요! 🎉
"""
    
    result = send_telegram_message(message)
    print(f"알림 전송 결과: {result}")
    return result

def notify_live_end(channel_name):
    """방송 종료 알림"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    message = f"""
⚫ <b>방송이 종료되었습니다</b>

📺 채널: {channel_name}
⏰ 종료 시간: {now}

다음 방송을 기대해주세요! 👋
"""
    
    result = send_telegram_message(message)
    print(f"알림 전송 결과: {result}")
    return result

def monitor_broadcast():
    """방송 상태를 지속적으로 모니터링합니다"""
    import time
    
    last_live_status = None
    channel_name = "암본이수혁 aguking"
    
    print("방송 모니터링 시작...")
    
    while True:
        try:
            # 방송 상태 확인 (예시 JSON)
            # 실제 API 에 따라 수정 필요
            status_data = {
                "ok": True,
                "live": False,  # 이 값이 변경됨
                "reset": False,
                "resetDate": None,
                "channel": channel_name
            }
            
            current_live = status_data.get("live", False)
            
            # 상태 변경 감지
            if last_live_status is not None and current_live != last_live_status:
                if current_live:
                    print("🔴 방송 시작 감지!")
                    notify_live_start(channel_name)
                else:
                    print("⚫ 방송 종료 감지!")
                    notify_live_end(channel_name)
            
            last_live_status = current_live
            
            # 30 초마다 확인
            time.sleep(30)
            
        except Exception as e:
            print(f"오류 발생: {e}")
            time.sleep(30)

if __name__ == "__main__":
    # 테스트 메시지 전송
    print("텔레그램 봇 테스트...")
    test_message = "👋 봇이 정상 작동합니다!"
    result = send_telegram_message(test_message)
    print(f"테스트 결과: {result}")
    
    # 모니터링 시작 (주석 해제하면 실행)
    # monitor_broadcast()
