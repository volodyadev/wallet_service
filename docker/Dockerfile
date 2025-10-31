FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y \
    python3.11 python3.11-distutils python3.11-venv python3-pip \
    build-essential libssl-dev libffi-dev libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /src

COPY requirements.txt .

RUN python3.11 -m pip install --upgrade pip \
    && python3.11 -m pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3.11", "-u", "main.py"]
