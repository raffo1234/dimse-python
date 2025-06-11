# Base image
FROM python:3.11-slim

# Avoid prompts during install
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    iputils-ping netcat curl gnupg libffi-dev build-essential \
    --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# ✅ Install Tailscale (official script, latest method)
RUN curl -fsSL https://tailscale.com/install.sh | sh

# Set working directory
WORKDIR /app

# Copy app files
COPY . /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entrypoint
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Start the app
CMD ["/start.sh"]
