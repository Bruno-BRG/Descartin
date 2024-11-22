import sqlite3
import json
from datetime import datetime

def connect_db():
    return sqlite3.connect('data.db')

def create_table():
    with connect_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS weights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                weight TEXT NOT NULL,
                residue_type TEXT NOT NULL,
                date TEXT NOT NULL
            )
        ''')
        conn.commit()

def load_data():
    with connect_db() as conn:
        cursor = conn.execute('SELECT * FROM weights')
        data = [{"id": row[0], "weight": row[1], "residue_type": row[2], "date": row[3]} for row in cursor.fetchall()]
    return data

def get_weight(index):
    with connect_db() as conn:
        cursor = conn.execute('SELECT * FROM weights WHERE id = ?', (index,))
        row = cursor.fetchone()
        if row:
            return {"id": row[0], "weight": row[1], "residue_type": row[2], "date": row[3]}
        else:
            return {"error": "Index out of range"}

def add_weight(weight, residue_type, date):
    with connect_db() as conn:
        conn.execute('INSERT INTO weights (weight, residue_type, date) VALUES (?, ?, ?)', (weight, residue_type, date))
        conn.commit()
    return {"message": "Weight added successfully"}

def update_weight(index, weight):
    with connect_db() as conn:
        conn.execute('UPDATE weights SET weight = ? WHERE id = ?', (weight, index))
        conn.commit()
    return {"message": "Weight updated successfully"}

def delete_weight(index):
    with connect_db() as conn:
        conn.execute('DELETE FROM weights WHERE id = ?', (index,))
        conn.commit()
    return {"message": "Weight deleted successfully"}

def populate_db_from_json(json_filepath):
    with open(json_filepath, 'r') as file:
        data = json.load(file)
    with connect_db() as conn:
        for entry in data:
            weight = entry['weight']
            residue_type = entry.get('residue_type', 'unknown')  # Default to 'unknown' if not provided
            date = entry.get('date', datetime.now().strftime('%Y-%m-%d'))  # Default to current date if not provided
            conn.execute('INSERT INTO weights (weight, residue_type, date) VALUES (?, ?, ?)', (weight, residue_type, date))
        conn.commit()
