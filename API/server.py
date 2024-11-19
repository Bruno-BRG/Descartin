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

@app.route('/api/residues/<int:residue_id>', methods=['PUT', 'DELETE'])
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

@app.route('/api/generate_graph', methods=['POST'])
def generate_graph():
    data = request.get_json()
    residue_type = data['residue_type']
    time_range = data.get('time_range', 'all_time')
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT MIN(date) as start_date, MAX(date) as end_date FROM residues WHERE residue_type = ?', (residue_type,))
        date_range = cursor.fetchone()
        conn.close()
        
        if not date_range['start_date'] or not date_range['end_date']:
            raise ValueError("No data available for the specified residue type")
        
        if time_range == 'last_year':
            start_date = (pd.to_datetime(date_range['end_date']) - pd.DateOffset(years=1)).strftime('%Y-%m-%d')
            end_date = date_range['end_date']
        elif time_range == 'last_month':
            start_date = (pd.to_datetime(date_range['end_date']) - pd.DateOffset(months=1)).strftime('%Y-%m-%d')
            end_date = date_range['end_date']
        else:  # all_time
            start_date = date_range['start_date']
            end_date = date_range['end_date']
        
        app.logger.info(f"Generating graph for residue_type: {residue_type}, start_date: {start_date}, end_date: {end_date}")
        
        # Clear the images folder
        images_folder = os.path.join(os.path.dirname(__file__), 'images')
        if os.path.exists(images_folder):
            for filename in os.listdir(images_folder):
                file_path = os.path.join(images_folder, filename)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
        
        # Call the math.py script
        script_path = os.path.join(os.path.dirname(__file__), 'math.py')
        result = subprocess.run(['python', script_path, residue_type, start_date, end_date], capture_output=True, text=True, check=True)
        file_path = result.stdout.strip()
        
        # Check if the file path is valid
        if not file_path or not os.path.exists(file_path):
            raise FileNotFoundError(f"Generated file not found: {file_path}")
        
        filename = os.path.basename(file_path)
        return jsonify({"filename": filename})
    except subprocess.CalledProcessError as e:
        app.logger.error(f"Error calling math.py: {e.stderr}")
        return jsonify({"error": f"Error calling math.py: {e.stderr}"}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/generate_bar_chart', methods=['POST'])
def generate_bar_chart():
    data = request.get_json()
    residue_types = data['residue_types']
    time_range = data.get('time_range', 'all_time')
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT MIN(date) as start_date, MAX(date) as end_date FROM residues')
        date_range = cursor.fetchone()
        conn.close()
        
        if not date_range['start_date'] or not date_range['end_date']:
            raise ValueError("No data available")
        
        if time_range == 'last_year':
            start_date = (pd.to_datetime(date_range['end_date']) - pd.DateOffset(years=1)).strftime('%Y-%m-%d')
            end_date = date_range['end_date']
        elif time_range == 'last_month':
            start_date = (pd.to_datetime(date_range['end_date']) - pd.DateOffset(months=1)).strftime('%Y-%m-%d')
            end_date = date_range['end_date']
        else:  # all_time
            start_date = date_range['start_date']
            end_date = date_range['end_date']
        
        app.logger.info(f"Generating bar chart for residue_types: {residue_types}, start_date: {start_date}, end_date: {end_date}")
        
        # Fetch data for the selected residue types and time range
        conn = get_db_connection()
        query = '''
        SELECT residue_type, weight, date FROM residues
        WHERE residue_type IN ({}) AND date BETWEEN ? AND ?
        '''.format(','.join('?' * len(residue_types)))
        params = residue_types + [start_date, end_date]
        data = pd.read_sql_query(query, conn, params=params)
        conn.close()
        
        if data.empty:
            raise ValueError("No data available for the selected parameters")
        
        # Save the data to a temporary CSV file
        temp_csv_path = os.path.join(os.path.dirname(__file__), 'temp_data.csv')
        data.to_csv(temp_csv_path, index=False)
        
        # Clear the images folder
        images_folder = os.path.join(os.path.dirname(__file__), 'images')
        if os.path.exists(images_folder):
            for filename in os.listdir(images_folder):
                file_path = os.path.join(images_folder, filename)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
        
        # Call the math.py script
        script_path = os.path.join(os.path.dirname(__file__), 'math.py')
        result = subprocess.run(['python', script_path, 'plot_bar_chart', temp_csv_path], capture_output=True, text=True, check=True)
        file_path = result.stdout.strip()
        
        # Remove the temporary CSV file
        os.remove(temp_csv_path)
        
        # Check if the file path is valid
        if not file_path or not os.path.exists(file_path):
            raise FileNotFoundError(f"Generated file not found: {file_path}")
        
        filename = os.path.basename(file_path)
        return jsonify({"filename": filename})
    except subprocess.CalledProcessError as e:
        app.logger.error(f"Error calling math.py: {e.stderr}")
        return jsonify({"error": f"Error calling math.py: {e.stderr}"}), 500
    except ValueError as e:
        app.logger.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/images/<filename>')
def get_image(filename):
    return send_file(os.path.join('images', filename), mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True, port=5001)