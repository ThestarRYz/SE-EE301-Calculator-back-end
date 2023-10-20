from flask import Flask, jsonify, request
import pymysql
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

# MySQL数据库连接配置
db = pymysql.connect(
    host='localhost',
    user='root',
    password='1234567z',
    database='calculator_db'
)
cursor = db.cursor()

# 创建数据库表
def create_table():
    sql = """CREATE TABLE IF NOT EXISTS history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                expression VARCHAR(255) NOT NULL,
                result DECIMAL(10,2) NOT NULL
            )"""
    cursor.execute(sql)
    db.commit()

# 插入历史记录
def insert_history(expression, result):
    sql = "INSERT INTO history (expression, result) VALUES (%s, %s)"
    cursor.execute(sql, (expression, result))
    db.commit()

# 获取历史记录
def get_history():
    sql = "SELECT * FROM history ORDER BY id DESC LIMIT 10"
    cursor.execute(sql)
    data = cursor.fetchall()
    return data

# 路由：获取历史记录API
@app.route('/api/calculator/history', methods=['GET'])
def get_history_api():
    data = get_history()
    history = [{'id': item[0], 'expression': item[1], 'result': float(item[2])} for item in data]
    return jsonify({
        "code": 200,
        "message": "ok",
        "data": {
            "history": history
            }
    })


@app.route('/api/calculator/history', methods=["POST"])
def store_result():
    expression = request.form.get("expression")
    result = request.form.get("result")
    print(expression, result)
    insert_history(expression, result)
    
    return jsonify({
        "code": 200,
        "message": "ok",
        "data": None
    })


if __name__ == '__main__':
    create_table()
    app.run()

