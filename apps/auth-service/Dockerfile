# Stage 1: Build
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Stage 2: Run
FROM python:3.11-slim

WORKDIR /app
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH="/root/.local/bin:${PATH}"

EXPOSE 8082

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8082"]
