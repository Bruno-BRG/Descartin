# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Install necessary system packages
RUN apt-get update && apt-get install -y \
    python3-distutils \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV FLASK_APP=server.py

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]