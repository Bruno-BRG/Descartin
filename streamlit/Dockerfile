FROM python:3.12.3-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install setuptools wheel && pip install protobuf==3.20.* && pip install -r requirements.txt

COPY . .

EXPOSE 8501

ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
