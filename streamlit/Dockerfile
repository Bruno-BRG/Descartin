FROM python:3.12-slim

WORKDIR /app

# Install required system packages
RUN apt-get update && apt-get install -y build-essential python3.12-distutils python3.12-dev python3-pip python3-setuptools

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
