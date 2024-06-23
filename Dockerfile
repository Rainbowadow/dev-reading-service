# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12.3
FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Download dependencies as a separate step to take advantage of Docker's caching
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Create cache directory for transformers and set environment variable
RUN mkdir -p /app/hf_home
ENV HF_HOME=/app/hf_home

# Run script to download model
COPY download_model.py .
RUN --mount=type=cache,target=/root/.cache/huggingface \
    python download_model.py

# Switch to the non-privileged user to run the application
USER appuser

# Copy the application code and the templates directory
COPY dev_service.py .
COPY templates/ templates/

EXPOSE 8080
CMD ["gunicorn", "dev_service:app", "--bind", "0.0.0.0:8080", "--access-logfile", "-", "--error-logfile", "-"]
