
// 기존 메시지 생성 폼 이벤트 리스너
document.getElementById('messageForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    const message = document.getElementById('message').value;
    const keyword = document.getElementById('keyword').value;

    try {
        const response = await fetch('http://127.0.0.1:5000/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message, keyword }),
        });

        const data = await response.json();

        if (response.ok) {
            const resultPlaceholder = document.querySelector('.result-placeholder');
            const placeholderWrapper = document.querySelector('.placeholder-wrapper');

            resultPlaceholder.innerHTML = '';  // 기존 내용 비우기
            placeholderWrapper.classList.add('start');  // 정렬을 위쪽으로 변경

            data.result_message.forEach((msg, index) => {
                const messageBox = document.createElement('div');
                messageBox.className = 'message-box';

                messageBox.innerHTML = `
                            <p><strong>예시 ${index + 1}:</strong></p>
                            <p>${msg}</p>
                            <div class="button-group">
                                <button class="btn-delete">삭제</button>
                                <button class="btn-save">내 문자함 저장</button>
                                <button class="btn-use">메시지 사용</button>
                            </div>`;

                resultPlaceholder.appendChild(messageBox);

                // 삭제 버튼 이벤트 리스너 추가
                messageBox.querySelector('.btn-delete').addEventListener('click', () => {
                    resultPlaceholder.removeChild(messageBox);

                    // 모든 메시지가 삭제되면 정렬을 원래대로 되돌림
                    if (resultPlaceholder.children.length === 0) {
                        placeholderWrapper.classList.remove('start');
                        resultPlaceholder.innerHTML = `
                                    생성결과가 없습니다.<br>뿌리오 AI 기능을 이용해보세요!
                                `;
                    }
                });

                messageBox.querySelector('.btn-save').addEventListener('click', () => {
                    alert('메시지가 저장되었습니다!');
                });

                messageBox.querySelector('.btn-use').addEventListener('click', () => {
                    alert('이 메시지를 사용합니다!');
                });
            });
        } else {
            alert('문자 생성 실패: ' + (data.error || '알 수 없는 오류'));
        }
    } catch (error) {
        console.error('오류 발생:', error);
        alert('서버 요청 중 오류가 발생했습니다.');
    }
});

// 새로 추가하는 키워드 관리 로직
const keywordInput = document.getElementById('keyword');
const addKeywordButton = document.getElementById('addKeywordButton');
const keywordContainer = document.querySelector('.added-keywords');
let keywords = []; // 키워드를 저장할 배열

addKeywordButton.addEventListener('click', () => {
    const keyword = keywordInput.value.trim();

    if (keyword && keywords.length < 3) {
        keywords.push(keyword); // 배열에 키워드 추가
        renderKeywords(); // 키워드를 화면에 렌더링
        keywordInput.value = ''; // 입력창 초기화
    } else if (keywords.length >= 3) {
        alert('최대 3개의 키워드만 추가할 수 있습니다.');
    }
});

function renderKeywords() {
    keywordContainer.innerHTML = ''; // 기존 키워드 초기화

    keywords.forEach((kw, index) => {
        const keywordBox = document.createElement('div');
        keywordBox.className = 'keyword-box';
        keywordBox.innerHTML = `
                    ${kw} <span class="remove-keyword" data-index="${index}">&times;</span>
                `;

        // 삭제 버튼 클릭 시 이벤트
        keywordBox.querySelector('.remove-keyword').addEventListener('click', (e) => {
            const index = e.target.getAttribute('data-index');
            keywords.splice(index, 1); // 해당 키워드 삭제
            renderKeywords(); // 다시 렌더링
        });

        keywordContainer.appendChild(keywordBox); // 키워드 박스 추가
    });
}
