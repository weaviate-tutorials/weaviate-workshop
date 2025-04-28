FROM python:3.11-slim-bullseye
WORKDIR /workspaces/weaviate-workshop

# Install tools and utilities
RUN apt-get update && apt-get install -y \
    git \
    curl \
    vim \
    wget \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
