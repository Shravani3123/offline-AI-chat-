FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy dependency list
COPY requirements.txt .

# Update and install git with retry logic
RUN apt-get update \
 && apt-get install -y git \
 || (sleep 5 && apt-get update && apt-get install -y git) \
 && apt-get clean

# Upgrade pip and install dependencies
RUN pip install --upgrade pip \
 && pip install --prefer-binary --no-cache-dir torch==2.1.2+cpu -f https://download.pytorch.org/whl/torch_stable.html \
 && pip install --prefer-binary --no-cache-dir -r requirements.txt

# Copy the app code
COPY . .

# Default command
CMD ["python", "app/web_app.py"]
