from flask import Flask, request, jsonify, send_from_directory
import openai
import os
import re

app = Flask(__name__)
from flask_cors import CORS
CORS(app)  # CORS 설정을 통해 외부 도메인에서 API에 접근 가능하도록 허용

# OpenAI API 키 설정 (환경 변수에서 가져오기)
openai.api_key = ''

# HTML 파일 경로 설정
HTML_FOLDER = os.path.join(os.getcwd(), 'static', 'html')
STATIC_FOLDER = os.path.join(os.getcwd(), 'static')

def translate_result_message(message, keywords):
    prompt = (
        f"Write a single message for '{message}'."
        f"The message must use the keywords '{keywords[0]}', '{keywords[1]}', and '{keywords[2]}'. "
        f"The message must contains exactly 7 sentences."
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    # 메시지 내용을 추출
    return response['choices'][0]['message']['content'].strip()

@app.route('/generate', methods=['POST'])
def generate_text():
    try:
        data = request.json
        message = data.get('message', '제목 없음')
        keywords = data.get('keywords', [])

        # 리스트 형태가 아닐 경우 기본값 설정
        if not isinstance(keywords, list):
            keywords = ['키워드 없음', '키워드 없음', '키워드 없음']
        elif len(keywords) < 3:
            keywords.extend(['키워드 없음'] * (3 - len(keywords)))

        print(f"요청받은 데이터 - 제목: {message}, 키워드: {keywords[0]}, {keywords[1]}, {keywords[2]}")

        # 메시지 생성 로직
        result_message = translate_result_message(message, keywords)

        # UTF-8 기준 바이트 크기 계산
        byte_size = len(result_message.encode('utf-8'))
        print(f"최종 생성 결과: {result_message}")
        print(f"메시지 크기: {byte_size} 바이트")

        return jsonify({'result_message': [result_message]}), 200

    except Exception as e:
        # 예외 로그 출력
        print(f"오류 발생: {e}")
        return jsonify({'error': str(e)}), 500


# 정적 파일 제공
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(STATIC_FOLDER, filename)

# HTML 파일 제공
@app.route('/')
def serve_index():
    return send_from_directory(HTML_FOLDER, 'index.html')

# Flask 앱 실행
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)