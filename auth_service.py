from flask import Blueprint, request, jsonify
from flask_mysqldb import MySQL
import bcrypt

auth_service = Blueprint('auth_service', __name__)

# MySQL配置
mysql = MySQL()

@auth_service.route('/register', methods=['POST'])
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

@auth_service.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT id,password FROM users WHERE username = %s", (username,))
    user = cur.fetchone()

    if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
        return jsonify({"message": "Login successful!", "user_id": user[0]}), 200
    else:
        return jsonify({"error": "Invalid username or password!"}), 401