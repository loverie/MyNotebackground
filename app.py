from flask import Flask
from flask_mysqldb import MySQL
from auth_service import auth_service
from date_service import date_service
from task_service import task_service
app = Flask(__name__)

# MySQL配置
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Ma1212345'
app.config['MYSQL_DB'] = 'mynote'

mysql = MySQL(app)

# 注册蓝图
app.register_blueprint(auth_service)
app.register_blueprint(date_service)
app.register_blueprint(task_service)

if __name__ == '__main__':
    app.run(debug=True)