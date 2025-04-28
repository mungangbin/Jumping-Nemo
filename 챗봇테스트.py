from flask import Flask, request, jsonify

app = Flask(__name__)

# 기본 홈 페이지 (GET 요청)
@app.route("/", methods=["GET"])
def home():
    return "안녕하세요! Flask 챗봇 서버가 실행 중입니다."

# 카카오톡 메시지 처리 (POST 요청)
@app.route("/message", methods=["POST"])
def message():
    # 사용자가 보낸 메시지 받기
    data = request.get_json()
    print("📩 받은 데이터:", data)  # 터미널에 데이터 출력 (디버깅)

    user_msg = data["userRequest"]["utterance"]  # 사용자가 입력한 메시지 가져오기

    # 간단한 자동응답 로직
    if "안녕" in user_msg:
        bot_response = "안녕하세요! 만나서 반가워요 😊"
    elif "날씨" in user_msg:
        bot_response = "오늘 날씨는 맑아요! ☀️"
    else:
        bot_response = "무슨 말인지 잘 모르겠어요. 다시 한번 말씀해주세요!"

    # 카카오톡에서 요구하는 응답 형식
    response = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": bot_response
                    }
                }
            ]
        }
    }
    
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True, port=5000)