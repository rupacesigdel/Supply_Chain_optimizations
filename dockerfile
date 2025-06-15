FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/root/.cargo/bin:$PATH"

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libssl-dev \
    libffi-dev \
    pkg-config \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

RUN pip install --upgrade pip \
    && pip install mindsdb-sdk fluvio

WORKDIR /app
COPY . /app

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
