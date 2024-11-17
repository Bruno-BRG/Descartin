import sqlite3
import json

def create_table():
    conn = sqlite3.connect('data.db')
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

def insert_data(data):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    for item in data:
        cursor.execute('''
        INSERT INTO residues (date, residue_type, weight) VALUES (?, ?, ?)
        ''', (item['date'], item['Residue Type'], float(item['weight'].replace(',', ''))))
    conn.commit()
    conn.close()

def read_data():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM residues')
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_data(id, date, residue_type, weight):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE residues
    SET date = ?, residue_type = ?, weight = ?
    WHERE id = ?
    ''', (date, residue_type, weight, id))
    conn.commit()
    conn.close()

def delete_data(id):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM residues WHERE id = ?', (id,))
    conn.commit()
    conn.close()

def main():
    # Create table
    create_table()

if __name__ == "__main__":
    main()