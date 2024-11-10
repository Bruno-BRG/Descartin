from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    image_folder = os.path.join('static', 'Graphs')
    images = [f for f in os.listdir(image_folder) if f.endswith('.png') or f.endswith('.jpg')]
    return render_template('index.html', images=images)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

