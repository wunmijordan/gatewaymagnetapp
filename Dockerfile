# =========================
# Stage 0: Base Python Image
# =========================
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Working directory
WORKDIR /app

# =========================
# Stage 1: Install System Dependencies
# =========================
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libffi-dev \
    libcairo2 \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libgdk-pixbuf-xlib-2.0-0 \
    libgobject-2.0-0 \
    libssl-dev \
    git \
    wget \
    curl \
    shared-mime-info \
    fonts-liberation \
    && apt-get clean && rm -rf /var/lib/apt/lists/*


# =========================
# Stage 2: Copy and Install Python Dependencies
# =========================
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# =========================
# Stage 3: Copy Project Files
# =========================
COPY . /app/

# =========================
# Stage 4: Collect Static, Migrate, and Set Cloudinary Env
# =========================
# Set Cloudinary env vars here (replace with your actual values or use .env)
ENV CLOUDINARY_CLOUD_NAME=your_cloud_name
ENV CLOUDINARY_API_KEY=your_api_key
ENV CLOUDINARY_API_SECRET=your_api_secret

# Collect static files and run migrations
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

# =========================
# Stage 5: Expose Port & Start Gunicorn
# =========================
#CMD ["sh", "-c", "gunicorn gatewaymagnetapp.wsgi:application --bind 0.0.0.0:$PORT --workers=4 --threads=2 --timeout=120"]
