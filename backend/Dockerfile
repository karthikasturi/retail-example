# syntax=docker/dockerfile:1

# --- Build stage ---
FROM python:3.13.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies as non-root
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install --user --no-cache-dir -r requirements.txt

# --- Production image ---
FROM python:3.13.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/home/appuser/.local/bin:$PATH"

# Create non-root user
RUN useradd -m -u 1001 appuser

WORKDIR /app

# Install runtime dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /root/.local /home/appuser/.local
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages

# Copy application code
COPY app ./app
COPY requirements.txt ./requirements.txt

# Set permissions
RUN chown -R appuser:appuser /app /home/appuser/.local

# Expose port (default FastAPI port)
EXPOSE 8000

# Healthcheck (optional)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl --fail http://localhost:8000/health || exit 1

# Switch to non-root user
USER appuser

# Start the FastAPI app with Uvicorn
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
