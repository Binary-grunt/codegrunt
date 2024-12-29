FROM python:3.11-slim AS base
LABEL maintainer="binarygrunt"

ENV PYTHONUNBUFFERED=1 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PATH="/py/bin:$PATH"

# Define the argument for dev mode (true/false)
ARG DEV=false

# Set the working directory
WORKDIR /app

# Copy only the requirements files first to take advantage of the Docker cache
COPY requirements.txt /tmp/requirements.txt
COPY requirements.dev.txt /tmp/requirements.dev.txt

# Install minimal system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies in a virtual environment
RUN python -m venv /py && \
    /py/bin/pip install --no-cache-dir --upgrade pip && \
    /py/bin/pip install --no-cache-dir -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; then \
        /py/bin/pip install --no-cache-dir -r /tmp/requirements.dev.txt; \
    fi && \
    rm -rf /tmp

# Do NOT copy the application code here; it will be mounted as a volume
# Add a non-root user for security
RUN adduser --disabled-password --no-create-home codegruntuser
USER codegruntuser

# Update PATH to use /py/bin
ENV PATH="/py/bin:$PATH"

EXPOSE 8000

# Set the default command
# The code will be mounted from the host, so just run main.py from there
CMD ["python", "main.py"]
