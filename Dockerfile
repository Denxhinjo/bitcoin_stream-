# Use official Python image with pre-compiled packages
FROM python:3.10-slim-buster

# Set working directory
WORKDIR /app

# Install system dependencies in one RUN layer
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies with faster pip options
ENV PIP_NO_BACKTRACK=1
RUN pip install --no-cache-dir \
    --default-timeout=100 \
    --disable-pip-version-check \
    --no-warn-script-location \
    -r requirements.txt

# Copy application files
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Default command (overridden in compose)
CMD ["streamlit", "run", "dashboard_coinbase.py"]