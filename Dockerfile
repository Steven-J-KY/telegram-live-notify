FROM python:3.11-slim

WORKDIR /app

# 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 봇 코드 복사
COPY telegram_bot.py .

# 로그 디렉토리 생성
RUN mkdir -p /app/logs

# 환경 변수 설정 (선택적)
ENV PYTHONUNBUFFERED=1

# 봇 실행
CMD ["python", "telegram_bot.py"]
