from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_FILE = 'aceest.db'

def init_db():
    # Initialize the database and tables
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            age INTEGER,
            weight REAL,
            program TEXT,
            calories INTEGER
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT,
            week TEXT,
            adherence INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Calculate calories based on the program logic from the original Tkinter app
def calculate_calories(weight, program):
    if program == "Fat Loss (FL)":
        return int(weight * 22)
    elif program == "Hypertrophy (HT)":
        return int(weight * 30)
    elif program == "General Fitness (GF)":
        return int(weight * 26)
    return 0

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "ACEest Fitness API is running."}), 200

@app.route('/client', methods=['POST'])
def add_client():
    data = request.json
    name = data.get('name')
    age = data.get('age')
    weight = data.get('weight')
    program = data.get('program')

    if not all([name, age, weight, program]):
        return jsonify({"error": "Missing data fields"}), 400

    calories = calculate_calories(float(weight), program)

    try:
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO clients (name, age, weight, program, calories) VALUES (?, ?, ?, ?, ?)",
            (name, age, weight, program, calories)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "Client already exists"}), 409
    finally:
        conn.close()

    return jsonify({"message": "Client added successfully", "calories": calories}), 201

@app.route('/client/<name>', methods=['GET'])
def get_client(name):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT name, age, weight, program, calories FROM clients WHERE name=?", (name,))
    row = cur.fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "Client not found"}), 404

    client_data = {
        "name": row[0],
        "age": row[1],
        "weight": row[2],
        "program": row[3],
        "calories": row[4]
    }
    return jsonify(client_data), 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)