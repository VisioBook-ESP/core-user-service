# Build stage
FROM python:3.13-slim AS builder
WORKDIR /app

COPY requirements.txt .
RUN python -m venv /venv && /venv/bin/pip install --upgrade pip \
    && /venv/bin/pip install --no-cache-dir -r requirements.txt

COPY . .

# Production stage
FROM python:3.13-slim AS production
WORKDIR /app

RUN addgroup --system appgroup && adduser --system --uid 1001 --ingroup appgroup appuser

COPY --from=builder /venv /venv
COPY app ./app

ENV PATH=/venv/bin:$PATH
ENV PYTHONPATH=/app

USER appuser
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request,sys; sys.exit(0) if urllib.request.urlopen('http://localhost:8080/health').getcode()==200 else sys.exit(1)"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
