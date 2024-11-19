from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
import sqlite3
import pandas as pd
import subprocess
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database connection
def get_db_connection():
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'data.db'))
    conn.row_factory = sqlite3.Row
    return conn

# Create table if it doesn't exist
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS residues (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        residue_type TEXT,
        weight REAL
    )
    ''')
    conn.commit()
    conn.close()

create_table()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/residues/', methods=['GET', 'POST'])
def residues():
    if request.method == 'POST':
        data = request.get_json()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO residues (date, residue_type, weight) VALUES (?, ?, ?)
        ''', (data['date'], data['residue_type'], data['weight']))
        conn.commit()
        conn.close()
        return jsonify(data), 201
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM residues')
        rows = cursor.fetchall()
        conn.close()
        return jsonify([dict(row) for row in rows])

@app.route('/residue_types/', methods=['GET'])
def residue_types():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT residue_type FROM residues')
    rows = cursor.fetchall()
    conn.close()
    return jsonify([row['residue_type'] for row in rows])

@app.route('/residues/<int:residue_id>', methods=['PUT', 'DELETE'])
def update_delete_residue(residue_id):
    if request.method == 'PUT':
        data = request.get_json()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
        UPDATE residues
        SET date = ?, residue_type = ?, weight = ?
        WHERE id = ?
        ''', (data['date'], data['residue_type'], data['weight'], residue_id))
        conn.commit()
        conn.close()
        return jsonify({"message": "Residue updated successfully"})
    elif request.method == 'DELETE':
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM residues WHERE id = ?', (residue_id,))
        conn.commit()
        conn.close()
        return jsonify({"message": "Residue deleted successfully"})

@app.route('/residues/graph_data/')
def get_graph_data():
    residue_type = request.args.get('residue_type')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    conn = get_db_connection()
    query = '''
    SELECT date, weight FROM residues
    WHERE residue_type = ? AND date BETWEEN ? AND ?
    '''
    data = pd.read_sql_query(query, conn, params=(residue_type, start_date, end_date))
    conn.close()
    data['date'] = pd.to_datetime(data['date'])
    data = data.resample('MS', on='date').sum().reset_index()
    return jsonify(data.to_dict(orient='records'))

@app.route('/generate_graph', methods=['POST'])
def generate_graph():
    data = request.get_json()
    residue_type = data['residue_type']
    start_date = data['start_date']
    end_date = data['end_date']
    
    try:
        app.logger.info(f"Generating graph for residue_type: {residue_type}, start_date: {start_date}, end_date: {end_date}")
        # Call the math.py script
        result = subprocess.run(['python', 'math.py', residue_type, start_date, end_date], capture_output=True, text=True, check=True)
        file_path = result.stdout.strip()
        
        # Check if the file path is valid
        if not file_path or not os.path.exists(file_path):
            raise FileNotFoundError(f"Generated file not found: {file_path}")
        
        return send_file(file_path, mimetype='image/png')
    except subprocess.CalledProcessError as e:
        app.logger.error(f"Error calling math.py: {e.stderr}")
        return jsonify({"error": f"Error calling math.py: {e.stderr}"}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)