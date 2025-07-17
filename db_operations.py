import sqlite3
from datetime import datetime
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def init_db():
    with sqlite3.connect('hospital.db') as conn:
        c = conn.cursor()
        # Create patients table
        c.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER,
                status TEXT NOT NULL,
                date TEXT NOT NULL,
                scd_type INTEGER NOT NULL,
                is_current BOOLEAN DEFAULT 1,
                valid_from TEXT,
                valid_to TEXT,
                previous_status TEXT
            )
        ''')
        conn.commit()

def add_record(name, age, status, date, scd_type):
    with sqlite3.connect('hospital.db') as conn:
        c = conn.cursor()
        
        if scd_type == 1:  # SCD Type 1 - Direct Update
            c.execute('''
                INSERT OR REPLACE INTO patients (name, age, status, date, scd_type, is_current)
                VALUES (?, ?, ?, ?, ?, 1)
            ''', (name, age, status, date, scd_type))
            
        elif scd_type == 2:  # SCD Type 2 - Keep History
            # Set current record to not current
            c.execute('''
                UPDATE patients 
                SET is_current = 0, valid_to = ?
                WHERE name = ? AND scd_type = 2 AND is_current = 1
            ''', (date, name))
            
            # Insert new record
            c.execute('''
                INSERT INTO patients (name, age, status, date, scd_type, is_current, valid_from, valid_to)
                VALUES (?, ?, ?, ?, 2, 1, ?, NULL)
            ''', (name, age, status, date, date))
            
        elif scd_type == 3:  # SCD Type 3 - Keep Previous
            # Get current status before update
            c.execute('SELECT status FROM patients WHERE name = ? AND scd_type = 3', (name,))
            result = c.fetchone()
            prev_status = result[0] if result else None
            
            # Insert/Update record with previous status
            c.execute('''
                INSERT OR REPLACE INTO patients 
                (name, age, status, date, scd_type, previous_status, is_current)
                VALUES (?, ?, ?, ?, 3, ?, 1)
            ''', (name, age, status, date, prev_status))
            
        conn.commit()

def get_records(scd_type=None):
    with sqlite3.connect('hospital.db') as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        if scd_type:
            c.execute('SELECT * FROM patients WHERE scd_type = ?', (scd_type,))
        else:
            c.execute('SELECT * FROM patients')
            
        rows = c.fetchall()
        return [dict(row) for row in rows]

def delete_record(record_id, scd_type):
    with sqlite3.connect('hospital.db') as conn:
        c = conn.cursor()
        
        # Only delete if status is Positive
        c.execute('''
            DELETE FROM patients 
            WHERE patient_id = ? AND status = 'Positive' AND scd_type = ?
        ''', (record_id, scd_type))
        conn.commit()
        return c.rowcount > 0

# Flask routes
@app.route('/init', methods=['POST'])
def initialize_db():
    init_db()
    return jsonify({"message": "Database initialized successfully"})

@app.route('/patients', methods=['GET'])
def get_patients():
    scd_type = request.args.get('scd_type', type=int)
    records = get_records(scd_type)
    return jsonify(records)

@app.route('/patients', methods=['POST'])
def add_patient():
    data = request.json
    add_record(
        data['name'],
        data.get('age'),  # age is optional
        data['status'],
        data['date'],
        data['scd_type']
    )
    return jsonify({"message": "Patient added successfully"})

@app.route('/patients/<int:record_id>', methods=['DELETE'])
def delete_patient(record_id):
    scd_type = request.args.get('scd_type', type=int)
    if delete_record(record_id, scd_type):
        return jsonify({"message": "Patient deleted successfully"})
    return jsonify({"message": "Patient not found or not positive"}), 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
