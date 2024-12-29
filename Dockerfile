FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p uploads logs data/reference_signals data/test_samples

# Generate sample data
RUN python signal_generator.py

# Expose port
EXPOSE 9999

# Run application
CMD ["python", "app.py"]
