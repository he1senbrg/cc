# root/backend/Dockerfile
FROM python:3.13.7-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# INSTALL REQUIRED SYSTEM LIBRARIES
# libgomp1 is CRITICAL for scikit-learn/numpy on slim images
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libgomp1 \ 
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# drop privileges
RUN useradd -m appuser && chown -R appuser /app
USER appuser

EXPOSE 8000

# OPTIMIZED CMD FOR LOW MEMORY
# Changed --workers to 1 to prevent OOM
# Added --timeout 120 because ML predictions can sometimes be slow
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000", "--workers", "1", "--timeout", "120"]
