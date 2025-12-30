# Use updated Python base image with current Debian version
FROM python:3.11-slim-bullseye

ARG BUILD_ENV=prod
ENV BUILD_ENV=${BUILD_ENV}

# Set the working directory to /app
WORKDIR /app

# Install poetry via pip (more reliable than external script)
RUN pip install --no-cache-dir "poetry>=2.0,<3.0"

# Add Poetry to PATH
ENV PATH="/root/.local/bin:${PATH}"

# Install OSV Scanner for CVE scanning in development builds
RUN if [ "$BUILD_ENV" = "develop" ]; then \
    apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    curl -L https://github.com/google/osv-scanner/releases/latest/download/osv-scanner_linux_amd64 -o /usr/local/bin/osv-scanner && \
    chmod +x /usr/local/bin/osv-scanner; \
    fi

# Copy only the dependency files first to leverage Docker cache
COPY pyproject.toml poetry.lock README.md tox.ini ./

# Install project dependencies
RUN poetry config virtualenvs.create false && \
    if [ "$BUILD_ENV" = "develop" ]; then \
    poetry install --with dev --no-interaction --no-root; \
    else \
    poetry install --without dev --no-interaction --no-root; \
    fi

# Copy application code from cicd_practice directory (maintaining internal structure)
COPY cicd_practice ./cicd_practice

# Run as non-root user
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application (path remains consistent within container)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "cicd_practice.app:app"]
