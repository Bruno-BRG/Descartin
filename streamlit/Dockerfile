FROM python:3.12-slim

WORKDIR /app

# Install required system packages
RUN apt-get update && apt-get install -y python3-distutils build-essential python3-dev python3-pip python3-setuptools

# Ensure distutils is available
RUN apt-get install -y python3-distutils

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
