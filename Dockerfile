FROM python:3.11

WORKDIR /app

# 빌드 인자 설정: GitHub Secrets에서 전달받을 API Key와 Endpoint
ARG AZURE_OPENAI_API_KEY
ARG AZURE_OPENAI_ENDPOINT

# 빌드 인자를 ENV 변수로 설정
ENV AZURE_OPENAI_API_KEY=${AZURE_OPENAI_API_KEY}
ENV AZURE_OPENAI_ENDPOINT=${AZURE_OPENAI_ENDPOINT}

# Streamlit 관련 환경 변수 설정
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_RUN_ON_SAVE=false

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

# Streamlit 앱 실행 명령어로 변경
CMD ["streamlit", "run", "job_interviewer.py", "--server.port=8501", "--server.address=0.0.0.0"]
