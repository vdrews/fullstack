from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="HYEeo091/&$",
    database="demo_app"
)

cursor = db.cursor()

@app.route('/', methods=['GET'])
def home():
    return "welcome home"


# Add student
@app.route('/add-student', methods=['POST'])
def add_student():

    data = request.json
    name = data['name']
    email = data['email']

    sql = "INSERT INTO students (name, email) VALUES (%s,%s)"
    cursor.execute(sql,(name,email))
    db.commit()

    return jsonify({"message":"Student added"})

# Get all students
@app.route('/students', methods=['GET'])
def get_students():

    cursor.execute("SELECT * FROM students")
    result = cursor.fetchall()

    students = []

    for row in result:
        students.append({
            "id": row[0],
            "name": row[1],
            "email": row[2]
        })

    return jsonify(students)

app.run(debug=True)