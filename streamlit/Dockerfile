FROM python:3.12.3-slim

WORKDIR /app

# Install the latest version of pip, setuptools, and wheel
RUN pip install --upgrade pip setuptools wheel

# Install each package separately
RUN pip install streamlit
RUN pip install requests
RUN pip install pandas
RUN pip install matplotlib
RUN pip install scikit-learn
RUN pip install numpy

COPY . .

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
