#i want to host a flask server that will call a html file and display it on the browser i want all the png from the 2014Graphs folder to be displayed on the browser
# iwant to disply all the png files in the 2014Graphs folder in the main page the index.html

from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Ensure the directory exists
    directory = 'static/2014Graphs'
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # List all PNG files in the static/2014Graphs directory
    files = [f for f in os.listdir(directory) if f.endswith('.png')]
    return render_template('index.html', files=files)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

