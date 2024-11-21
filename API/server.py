from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
import sqlite3
import pandas as pd
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

@app.route('/api/residues/', methods=['GET', 'POST'])
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

@app.route('/api/residue_types/', methods=['GET'])
def residue_types():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT residue_type FROM residues')
    rows = cursor.fetchall()
    conn.close()
    return jsonify([row['residue_type'] for row in rows])

@app.route('/api/residues/graph_data/')
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
    app.logger.info(f"Fetched data: {data.head()}")  # Debugging statement
    data['date'] = pd.to_datetime(data['date'], errors='coerce')
    if data['date'].isnull().any():
        app.logger.error(f"Invalid date format in data: {data[data['date'].isnull()]}")
    data.set_index('date', inplace=True)  # Ensure the DataFrame has a DateTimeIndex
    data = data.resample('MS').sum().reset_index()
    return jsonify(data.to_dict(orient='records'))

@app.route('/api/all_time_weight', methods=['GET'])
def all_time_weight():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT residue_type, SUM(weight) as total_weight FROM residues GROUP BY residue_type')
        data = cursor.fetchall()
        conn.close()

        if not data:
            raise ValueError("No data available")

        return jsonify([dict(row) for row in data])
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)