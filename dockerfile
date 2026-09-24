FROM python:3.13-slim AS builder
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

FROM python:3.13-slim AS runner
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

RUN useradd -u 8888 appuser && chown -R appuser:appuser /app
USER appuser

COPY --chown=appuser:appuser . .
EXPOSE 8000
CMD [ "daphne", "-b", "0.0.0.0", "-p", "8000", "core.asgi:application"]