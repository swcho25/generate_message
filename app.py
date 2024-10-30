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


# 텍스트를 지정된 언어로 번역하는 함수
def translate_text(text, target_language):
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": f"Translate '{text}' to {target_language}. Just print out the results."}]
    )
    return response.choices[0].message['content'].strip()

def translate_result_message(message, keyword, num_examples=3):
    prompt = (
        f"Generate {num_examples} different message templates for '{message}'. output only results."
        f"Include the keyword '{keyword}' where appropriate. "
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
        keyword = data.get('keyword', '내용 없음')
        
        print(f"요청받은 데이터 - 제목: {message}, 키워드: {keyword}")  # 요청 데이터 로그 출력
        
        # 문자 생성 로직
        result_message = translate_result_message(message, keyword)
        print(f"최종 생성 결과1: {result_message[0]}\n")  # 최종 결과를 터미널에 출력
        print(f"최종 생성 결과2: {result_message[1]}\n")  # 최종 결과를 터미널에 출력
        print(f"최종 생성 결과3: {result_message[2]}\n")  # 최종 결과를 터미널에 출력

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
