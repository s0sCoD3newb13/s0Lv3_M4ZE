from flask import Flask, render_template, jsonify
import main  # 실행하고자 하는 main.py를 임포트

app = Flask(__name__)

@app.route('/')
def index():
    # 사용자에게 보여줄 HTML 페이지 전달
    return render_template('index.html')

@app.route('/run-script', methods=['POST'])
def run_script():
    try:
        # main.py 안에 있는 특정 함수(예: start_logic)를 실행
        # 코드는 서버에서 돌고 결과만 result 변수에 담깁니다.
        result = main.start_logic() 
        return jsonify({"status": "success", "output": result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
