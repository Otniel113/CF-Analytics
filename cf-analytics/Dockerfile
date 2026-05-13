FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create a non-root user for security (recommended by HF)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app
COPY --chown=user . $HOME/app

# Expose the port HF Spaces expects
EXPOSE 7860

# Command to run the application
# --allow-websocket-origin=* is critical for HF Spaces
CMD ["panel", "serve", "app.py", "--address", "0.0.0.0", "--port", "7860", "--allow-websocket-origin=*", "--static-dirs", "assets=./assets"]
