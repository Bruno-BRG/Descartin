from flask import Flask, request, send_file
from flask_cors import CORS
import qrcode
import io
import json
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/generate-qrcode', methods=['POST'])
def generate_qrcode():
    data = request.json
    print("Received data:", data)  # Debugging statement
    battery_info = f"Model: {data['model']}, Capacity: {data['capacity']} kWh, Voltage: {data['voltage']} V, Manufacturer: {data['manufacturer']}"

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(battery_info)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')

    # Save the QR code image to a BytesIO object
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    # Save the battery information to data.json
    save_data_to_json(data)

    print("Sending QR code image")  # Debugging statement
    return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='qrcode.png')

def save_data_to_json(data):
    file_path = 'data.json'
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []

    existing_data.append(data)

    with open(file_path, 'w') as file:
        json.dump(existing_data, file, indent=4)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)