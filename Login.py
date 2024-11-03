from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import bcrypt
from datetime import datetime

app = Flask(__name__)

# MySQL配置
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Ma1212345'
app.config['MYSQL_DB'] = 'mynote'

mysql = MySQL(app)
@app.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']

    # 检查用户名是否已经存在
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    existing_user = cur.fetchone()

    if existing_user:
        return jsonify({"error": "Username already exists!"}), 400

    # 加密密码
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        mysql.connection.commit()
        return jsonify({"message": "User registered successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()

@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT password FROM users WHERE username = %s", (username,))
    user = cur.fetchone()

    if user and bcrypt.checkpw(password.encode('utf-8'), user[0].encode('utf-8')):
        return jsonify({"message": "Login successful!", "user_id": user[0]}), 200
    else:
        return jsonify({"error": "Invalid username or password!"}), 401

@app.route('/current_date', methods=['GET'])
def get_current_date():
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")  # 格式化为 YYYY-MM-DD
    current_weekday = now.strftime("%A")     # 获取星期几的名称
    return jsonify(date=current_date, weekday=current_weekday)


if __name__ == '__main__':
    app.run(debug=True)