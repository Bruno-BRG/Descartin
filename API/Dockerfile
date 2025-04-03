FROM python:3.12.3-slim

WORKDIR /app

COPY requirements.txt ./requirements.txt

# Install the latest version of setuptools and wheel
RUN pip install --upgrade pip setuptools wheel

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8050"]
