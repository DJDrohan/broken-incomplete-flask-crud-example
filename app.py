from flask import Flask, request, json, send_from_directory
from flask_cors import CORS
import psycopg2

app = Flask(__name__, static_folder='static')
CORS(app)

# PostgreSQL Instance configurations
# Change these details to match your instance configurations
app.config['DB_USER'] = 'postgres'
app.config['DB_PASSWORD'] = 'Sp00ky!'
app.config['DB_NAME'] = 'postgres'
app.config['DB_HOST'] = 'localhost'
app.config['DB_PORT'] = '5432'  # Default PostgreSQL port

def get_db_connection():
    return psycopg2.connect(
        user=app.config['DB_USER'],
        password=app.config['DB_PASSWORD'],
        database=app.config['DB_NAME'],
        host=app.config['DB_HOST'],
        port=app.config['DB_PORT']
    )

@app.route("/add", methods=['POST'])  # Add Student
def add():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO students(studentName, email) VALUES (%s, %s) RETURNING studentID;", (name, email))
        student_id = cursor.fetchone()[0]
        connection.commit()
        return json.dumps({'Result': 'Success', 'ID': student_id}), 201
    except Exception as e:
        return json.dumps({'Result': 'Error', 'Message': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route("/update/<int:student_id>", methods=['PUT'])  # Update Student
def update(student_id):
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("UPDATE students SET studentName = %s, email = %s WHERE studentID = %s;", (name, email, student_id))
        connection.commit()
        return '{"Result":"Success"}'
    except Exception as e:
        return '{"Result":"Error", "Message":"' + str(e) + '"}'
    finally:
        cursor.close()
        connection.close()

@app.route("/delete/<int:student_id>", methods=['DELETE'])  # Delete Student
def delete(student_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM students WHERE studentID = %s;", (student_id,))
        connection.commit()
        return '{"Result":"Success"}'
    except Exception as e:
        return '{"Result":"Error", "Message":"' + str(e) + '"}'
    finally:
        cursor.close()
        connection.close()

# Route for fetching data
@app.route("/read")
def read():
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM students;")
        results = cursor.fetchall()

        response = {'Results': [{'Name': row[1], 'Email': row[2], 'ID': row[0]} for row in results], 'count': len(results)}
        return app.response_class(
            response=json.dumps(response),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        return '{"Result":"Error", "Message":"' + str(e) + '"}'
    finally:
        cursor.close()
        connection.close()

# Default - Show Data
@app.route("/")
def index():
    return app.send_static_file('index.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080')
