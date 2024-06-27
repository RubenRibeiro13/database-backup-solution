# Use a Python base image
FROM python:3.9-slim

# Install necessary packages
RUN apt-get update && \
apt-get install -y postgresql-client && \
apt-get clean

# Set working directory inside the container
WORKDIR /app

# Copy the backup script to the '/app' directory in the container
COPY backup.py .

# Copy the entrypoint script to the '/app' directory in the container
COPY entrypoint.sh .

# Make entrypoint script executable
RUN chmod +x entrypoint.sh

# Set the entrypoint
ENTRYPOINT [ "/app/entrypoint.sh" ]