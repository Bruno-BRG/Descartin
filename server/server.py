from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    files = [f for f in os.listdir('/home/bubu/Documents/Descartin/server/static/Graphs') if f.endswith('.png')]
    return render_template('index.html', files=files)

if __name__ == '__main__':
    app.run(debug=True)

