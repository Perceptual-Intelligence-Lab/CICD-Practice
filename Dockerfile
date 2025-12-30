# Use updated Python base image with current Debian version
FROM python:3.11-slim-bullseye

# Set the working directory to /app
WORKDIR /app

# Install poetry via pip (more reliable than external script)
RUN pip install --no-cache-dir poetry

# Add Poetry to PATH
ENV PATH="/root/.local/bin:${PATH}"

# Copy only the dependency files first to leverage Docker cache
COPY pyproject.toml poetry.lock ./

# Install project dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --without dev --no-interaction --no-root

# Copy application code from cicd_practice directory (maintaining internal structure)
COPY cicd_practice ./cicd_practice

# Run as non-root user
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application (path remains consistent within container)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "cicd_practice.app:app"]
