from flask import Flask, jsonify, render_template
import sqlite3

app = Flask(__name__)

# 創建或連接 SQLite 資料庫
def connect_db():
    conn = sqlite3.connect('data.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS environment_data
           (id INTEGER PRIMARY KEY AUTOINCREMENT,
           timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
           temperature REAL,
           humidity REAL,
           air_quality TEXT,
           weather TEXT,
           electricity REAL);''')
    return conn

# 插入5筆假數據
def insert_fake_data():
    fake_data = [
        (24.5, 55.0, "良好", "晴天", 4.8),
        (26.0, 60.0, "普通", "陰天", 5.0),
        (25.0, 65.0, "不佳", "小雨", 5.5),
        (27.0, 70.0, "優良", "晴天", 6.0),
        (23.5, 50.0, "良好", "多雲", 4.3)
    ]
    
    conn = connect_db()
    for data in fake_data:
        conn.execute("INSERT INTO environment_data (temperature, humidity, air_quality, weather, electricity) VALUES (?, ?, ?, ?, ?)", data)
    conn.commit()
    conn.close()

@app.route('/update', methods=['POST'])
def update_data():
    # 假設這裡接收到樹莓派傳來的數據，並存儲在資料庫
    temperature = 25.0  # 這些數值應該從樹莓派來
    humidity = 60.0
    air_quality = "良好"
    weather = "晴天"
    electricity = 5.3
    
    conn = connect_db()
    conn.execute("INSERT INTO environment_data (temperature, humidity, air_quality, weather, electricity) VALUES (?, ?, ?, ?, ?)",
                 (temperature, humidity, air_quality, weather, electricity))
    conn.commit()
    conn.close()
    
    return "Data updated", 200

# 提供最新數據給前端
@app.route('/data')
def get_latest_data():
    conn = connect_db()
    cursor = conn.execute("SELECT * FROM environment_data ORDER BY timestamp DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    
    if row:
        data = {
            "temperature": row[2],
            "humidity": row[3],
            "air_quality": row[4],
            "weather": row[5],
            "electricity": row[6]
        }
    else:
        data = {}

    return jsonify(data)

# 提供歷史數據給前端
@app.route('/history')
def get_history_data():
    conn = connect_db()
    cursor = conn.execute("SELECT * FROM environment_data ORDER BY timestamp DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()
    
    history = []
    for row in rows:
        history.append({
            "timestamp": row[1],
            "temperature": row[2],
            "humidity": row[3],
            "air_quality": row[4],
            "weather": row[5],
            "electricity": row[6]
        })

    return jsonify(history)

# 渲染前端頁面
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    insert_fake_data()  # 插入假數據
    app.run(host='0.0.0.0', port=80)
