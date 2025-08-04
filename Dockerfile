FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
WORKDIR /app

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.maxUploadSize=2000", "--server.enableCORS=false", "--server.address=0.0.0.0"]
