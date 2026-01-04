# Use a lightweight Linux image with Python pre-installed
FROM python:3.12-slim

# Install GCC (The compiler you need for the test)
RUN apt-get update && apt-get install -y gcc

# Create a working directory
WORKDIR /app

# Copy your requirements and install them
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the rest of your code
COPY . /app/
