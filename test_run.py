from flask import Flask, request

app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def hello():
    name = request.args.get('name', '익명')  # 쿼리스트링에서 name 받기
    return f"안녕하세요, {name}님!"

if __name__ == '__main__':
    app.run(debug=True)
