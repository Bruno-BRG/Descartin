FROM python:3.12.3-slim

WORKDIR /app

# Install system dependencies required for Prophet
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["streamlit", "run", "app.py", "--server.port=69420", "--server.address=0.0.0.0"]
