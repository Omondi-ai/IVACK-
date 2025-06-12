# Stage 1: Build
FROM python:3.11-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc python3-dev libpq-dev && \
    rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

RUN groupadd -r appuser && \
    useradd -r -u 1001 -g appuser appuser

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY . .

RUN chmod +x /app/entrypoint.sh /app/wait-for-postgres.sh
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
