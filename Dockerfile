FROM python:3.11-slim

# Install required Python libraries
RUN pip install redis==5.2.1

# Set work directory
WORKDIR /app
