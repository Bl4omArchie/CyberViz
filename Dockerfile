FROM python:3.11-slim

COPY requirements.txt ./
RUN python3 -m venv env
RUN pip3 install --no-cache-dir -r requirements.txt

WORKDIR /app


EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.enableCORS=false", "--server.address=0.0.0.0"]
