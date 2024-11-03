from flask import Blueprint, jsonify,request
from datetime import datetime
from flask_mysqldb import MySQL

task_service = Blueprint('task_service', __name__)

# MySQL配置
mysql = MySQL()
@task_service.route('/pending_tasks', methods=['GET'])
def get_pending_tasks():
    user_id = request.args.get('user_id')  # 从查询参数中获取用户 ID
    today = datetime.now().date()

    # 查询未完成的事项数量
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT COUNT(*)
        FROM TaskContents tc
        INNER JOIN Tasks t ON tc.task_id = t.task_id
        WHERE tc.is_completed = FALSE AND t.task_date = %s AND t.user_id = %s
    """, (today, user_id))

    pending_count = cur.fetchone()[0]  # 获取查询结果中的数量

    cur.close()
    return jsonify(pending_tasks=pending_count), 200

@task_service.route('/add_task', methods=['POST'])
def add_task():
    data = request.get_json()

    # 如果输入是一个字典，转换为单元素列表
    if isinstance(data, dict):
        data = [data]

    user_id = request.args.get('user_id')  # 从请求参数中获取用户ID

    if not user_id:
        return jsonify(message='User ID is required'), 400

    if isinstance(data, list):
        for item in data:
            task_content = item.get('task_content')
            expected_completion_time = item.get('expected_completion_time')

            if not task_content or not expected_completion_time:
                return jsonify(message='Task content and expected completion time are required'), 400

            today = datetime.now().date()
            cur = mysql.connection.cursor()
            cur.execute("SELECT task_id FROM Tasks WHERE task_date = %s AND user_id = %s", (today, user_id))
            task = cur.fetchone()

            if task:
                task_id = task[0]
            else:
                cur.execute("INSERT INTO Tasks (user_id, task_date) VALUES (%s, %s)", (user_id, today))
                mysql.connection.commit()
                task_id = cur.lastrowid

            cur.execute("""
                INSERT INTO TaskContents (task_id, content_text, expected_completion_time)
                VALUES (%s, %s, %s)
            """, (task_id, task_content, expected_completion_time))
            mysql.connection.commit()

        cur.close()
        return jsonify(message='Tasks added successfully'), 200

    else:
        return jsonify(message='Invalid input format'), 400

@task_service.route('/user_pending_tasks', methods=['GET'])
def get_user_pending_tasks():
    # 获取用户ID，假设通过请求的查询参数传递用户ID
    user_id = request.args.get('user_id')
    print("user id=%d",user_id)
    if not user_id:
        return jsonify(message='User ID is required'), 400

    # 获取当前日期
    today = datetime.now().date()

    # 查询该用户当天的未完成事项
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT tc.content_text, tc.expected_completion_time
        FROM TaskContents tc
        INNER JOIN Tasks t ON tc.task_id = t.task_id
        WHERE tc.is_completed = FALSE AND t.task_date = %s AND t.user_id = %s
    """, (today, user_id))

    tasks = cur.fetchall()  # 获取所有查询结果
    cur.close()

    # 将结果转换为字典列表
    task_list = [{'content_text': task[0], 'expected_completion_time': task[1]} for task in tasks]

    return jsonify(pending_tasks=task_list), 200