FROM python:3.10-slim
WORKDIR /app
COPY bot.py .
RUN apt-get update && apt-get install -y curl && \
    pip install python-telegram-bot==13.15 apscheduler pytz && \
    apt-get clean
ENV PYTHONUNBUFFERED=1
CMD ["python", "bot.py"]

