# (베이스 이미지)
FROM python:3.9-slim

# (작업 디렉토리 설정)
WORKDIR /app

# (종속성 설치)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# (소스 코드 복사)
COPY . .

# (포트 노출)
EXPOSE 8000

# (명령 실행)
# 0.0.0.0은 외부에 연결 가능한 것을 의미
# 80: http
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]