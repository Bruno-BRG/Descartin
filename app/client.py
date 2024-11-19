from flask import Flask, render_template
import os
import shutil

app = Flask(__name__)

@app.route('/')
def index():
    # Clear the images folder
    images_folder = os.path.join(os.path.dirname(__file__), 'images')
    if os.path.exists(images_folder):
        shutil.rmtree(images_folder)
    os.makedirs(images_folder)
    
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)