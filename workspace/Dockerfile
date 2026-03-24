# Dockerfile for Physio-Concierge Demo

# Step 1: Use a base Python image
FROM python:3.10-slim

# Step 2: Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Step 3: Set the working directory
WORKDIR /app

# Step 4: Copy the project files into the container
COPY . /app/

# Step 5: Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 6: Command to run the demo
CMD ["python", "physio_concierge_demo.py"]