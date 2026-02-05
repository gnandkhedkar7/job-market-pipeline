FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency list
COPY requirements.txt .

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt \
    && playwright install chromium \
    && playwright install-deps


# Copy project code
COPY src ./src
COPY db ./db

# Ensure Python can find src/
ENV PYTHONPATH=/app

# Default command
CMD ["python", "-m", "src.scripts.run_pipeline"]