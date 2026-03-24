# Dockerfile per il Telegram Bot Physio-Concierge

# Step 1: Usa un'immagine Python leggera come base
FROM python:3.10-slim

# Step 2: Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Step 3: Set working directory
WORKDIR /app

RUN apt-get update && apt-get install -y g++ curl && apt-get clean
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g @google/gemini-cli && \
    mkdir -p /root/.gemini

# Step 4: Copy the bot files and requirements
COPY requirements.txt /app/requirements.txt
COPY telegram_bot.py /app/telegram_bot.py
COPY physio_concierge_demo.py /app/physio_concierge_demo.py

# Step 5: Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 6: Definisci il comando d'ingresso
CMD ["python", "telegram_bot.py"]