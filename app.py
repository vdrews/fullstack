from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

def get_db():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        port=int(os.environ.get("DB_PORT", 3306)),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME")
    )

@app.route('/', methods=['GET'])
def home():
    return "welcome home"

@app.route('/add-student', methods=['POST'])
def add_student():
    data = request.json
    name = data['name']
    email = data['email']

    db = get_db()
    cursor = db.cursor()
    sql = "INSERT INTO students (name, email) VALUES (%s,%s)"
    cursor.execute(sql, (name, email))
    db.commit()
    cursor.close()
    db.close()

    return jsonify({"message": "Student added"})

@app.route('/students', methods=['GET'])
def get_students():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM students")
    result = cursor.fetchall()
    cursor.close()
    db.close()

    students = []
    for row in result:
        students.append({
            "id": row[0],
            "name": row[1],
            "email": row[2]
        })

    return jsonify(students)



@app.route('/debug', methods=['GET'])
def debug():
    return jsonify({
        "host": os.environ.get("DB_HOST"),
        "port": os.environ.get("DB_PORT"),
        "user": os.environ.get("DB_USER"),
        "db": os.environ.get("DB_NAME"),
        "password_set": bool(os.environ.get("DB_PASSWORD"))
    })
