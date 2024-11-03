from flask import Blueprint, jsonify
from datetime import datetime

date_service = Blueprint('date_service', __name__)

@date_service.route('/current_date', methods=['GET'])
def get_current_date():
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")  # 格式化为 YYYY-MM-DD
    current_weekday = now.strftime("%A")     # 获取星期几的名称
    return jsonify(date=current_date, weekday=current_weekday)