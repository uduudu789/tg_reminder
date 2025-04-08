FROM python:3.10-slim
WORKDIR /app
RUN apt-get update && apt-get install -y curl && \
    pip install python-telegram-bot==13.15 apscheduler pytz && \
    apt-get clean
COPY bot.py .
ENV PYTHONUNBUFFERED=1
CMD ["python", "bot.py"]

