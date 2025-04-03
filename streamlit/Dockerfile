FROM python:3.12.3-slim

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt
RUN pip install streamlit
RUN pip install requests
RUN pip install pandas
RUN pip install matplotlib
RUN pip install scikit-learn
RUN pip install numpy
RUN pip install plotly

COPY . .

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
