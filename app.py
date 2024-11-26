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

def translate_result_message(message, keywords, num_examples=3):
    prompt = (
        f"Generate {num_examples} different message templates for '{message}'. output only results."
        f"Include the keywords '{keywords[0], keywords[1], keywords[2]}' where appropriate."
        f"Each message should be at least 500 bytes in length."
        f"Provide each example in the format '1. ...', '2. ...', '3. ...'."
    )
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    result = response.choices[0].message['content'].strip()
    # 정규식을 이용해 각 번호로 시작하는 부분을 기준으로 분리
    examples = re.split(r'\n?\d+\.\s', result)[1:]  # 첫 번째 빈 문자열 제거
    return examples  # 배열 반환

# 문자 자동 생성 API
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
        
        print(f"요청받은 데이터 - 제목: {message}, 키워드: {keywords[0], keywords[1], keywords[2]}")  # 요청 데이터 로그 출력
        
        # 문자 생성 로직
        result_message = translate_result_message(message, keywords)
        
        # 각 메시지와 바이트 크기를 로그에 출력
        for i, msg in enumerate(result_message, start=1):
            byte_size = len(msg.encode('utf-8'))  # UTF-8 기준 바이트 크기 계산
            print(f"최종 생성 결과 {i}: {msg}\n크기: {byte_size} 바이트\n")
        # 생성된 메시지를 반환
        return jsonify({'result_message': result_message}), 200

    except Exception as e:
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