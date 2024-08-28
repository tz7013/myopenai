from flask import Flask, request, render_template
import myopenai

app = Flask(__name__, static_folder='static', static_url_path='/static')

@app.route('/v1/hello')
def hello():
    return 'Hello Flask'

@app.route('/v1/chat')
def chat():
    msg = request.args.get('msg')
    return myopenai.aichat(msg)

@app.route('/')
def home():
    return render_template('index.html')

# 只在開發環境下使用 Flask 內建伺服器
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=10000)
