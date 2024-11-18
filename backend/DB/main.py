from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import pandas as pd

app = FastAPI()

# Pydantic models for request and response bodies
class Residue(BaseModel):
    date: str
    residue_type: str
    weight: float

class ResidueUpdate(BaseModel):
    id: int
    date: str
    residue_type: str
    weight: float

# Database connection
def get_db_connection():
    conn = sqlite3.connect('data.db')
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

@app.post("/residues/", response_model=Residue)
def create_residue(residue: Residue):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO residues (date, residue_type, weight) VALUES (?, ?, ?)
    ''', (residue.date, residue.residue_type, residue.weight))
    conn.commit()
    conn.close()
    return residue

@app.get("/residues/")
def read_residues():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM residues')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.put("/residues/{residue_id}")
def update_residue(residue_id: int, residue: ResidueUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE residues
    SET date = ?, residue_type = ?, weight = ?
    WHERE id = ?
    ''', (residue.date, residue.residue_type, residue.weight, residue_id))
    conn.commit()
    conn.close()
    return {"message": "Residue updated successfully"}

@app.delete("/residues/{residue_id}")
def delete_residue(residue_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM residues WHERE id = ?', (residue_id,))
    conn.commit()
    conn.close()
    return {"message": "Residue deleted successfully"}

@app.get("/residues/graph_data/")
def get_graph_data(residue_type: str, start_date: str, end_date: str):
    conn = get_db_connection()
    query = '''
    SELECT date, weight FROM residues
    WHERE residue_type = ? AND date BETWEEN ? AND ?
    '''
    data = pd.read_sql_query(query, conn, params=(residue_type, start_date, end_date))
    conn.close()
    data['date'] = pd.to_datetime(data['date'])
    data = data.resample('M', on='date').sum().reset_index()
    return data.to_dict(orient='records')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)