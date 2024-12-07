FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code/

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libffi-dev libssl-dev libmariadb-dev wait-for-it

# Install pipenv
RUN pip install --no-cache-dir pipenv

# Copy Pipfile and install dependencies
COPY Pipfile Pipfile.lock ./
RUN pipenv install --deploy --system

# Copy project files
COPY . /code/

# Expose ports
EXPOSE 8000
EXPOSE 3306
