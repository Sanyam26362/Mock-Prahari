FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MOCK_LATENCY=true \
    MOCK_LATENCY_MIN_MS=150 \
    MOCK_LATENCY_MAX_MS=400

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Create non-root user matching Hugging Face Spaces requirements (UID 1000)
RUN useradd -m -u 1000 user

# Copy application files
COPY --chown=user:user . .

# Set execution permissions on start script and make data folder writable
RUN chmod +x start.sh && \
    chown -R user:user /app

# Switch to non-root user
USER user

# Expose default Hugging Face Spaces port
EXPOSE 7860

# Run entrypoint script
CMD ["./start.sh"]
