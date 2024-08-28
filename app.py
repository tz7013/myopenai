from flask import Flask, request, send_file
import myopenai

# 初始化
app = Flask(__name__, static_folder='static', static_url_path='/static')

# 測試, 在網址後面加上/v1/hello, 網頁顯示'Hello Flask'
@app.route('/v1/hello')
def hello():
    return 'Hello Flask'

# 接受訊息並呼叫函式myopenai.aichat
@app.route('/v1/chat')
def chat():
    msg = request.args.get('msg')
    return myopenai.aichat(msg)

@app.route('/<path>')
def static_file(path):
    return send_file(f'templates/{path}')

@app.route('/')
def home():
    return send_file('templates/index.html')

# # 啟動flask server
# app.run(debug=True, port=80)    # 預設port=80, 在網址後面就不用加":port"
# 啟動 Gunicorn 來運行 Flask 應用程式
if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=10000)  # 不要用在生產環境