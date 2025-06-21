FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

RUN mkdir -p /tmp/matplotlib && chmod -R 777 /tmp/matplotlib

ENV MPLCONFIGDIR=/tmp/matplotlib

EXPOSE 7860

CMD ["uvicorn", "chatbot:app", "--host", "0.0.0.0", "--port", "7860"]