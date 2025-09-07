# ----------------------
# Stage 0: Base
# ----------------------
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies for WeasyPrint and general build
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libffi-dev \
    libcairo2 \
    libpango-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libgobject-2.0-0 \
    libffi-dev \
    libssl-dev \
    git \
    wget \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Collect static files and run migrations
# Cloudinary env vars need to be set in Railway settings or .env
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

# Expose the port your app runs on
EXPOSE 8000

# Command to run the app using Gunicorn
CMD ["gunicorn", "gatewaymagnetapp.wsgi:application", "--bind", "0.0.0.0:8000"]
