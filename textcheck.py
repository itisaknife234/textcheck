import requests
from bs4 import BeautifulSoup

def check_spelling_nara(text):
    # 1. 세션 생성 (첫 번째 요청)
    session = requests.Session()
    
    # User-Agent를 추가하여 브라우저 요청처럼 보이게 함
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "Referer": "https://nara-speller.co.kr/speller"
    }

    # 첫 페이지 요청 (세션 유지)
    session.get("https://nara-speller.co.kr/speller", headers=headers)

    # 2. 맞춤법 검사 요청 (두 번째 요청)
    url = "https://nara-speller.co.kr/speller/results"
    data = {
        "text1": text
    }

    response = session.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        result_text = extract_corrected_text(response.text)
        return result_text
    else:
        return f"오류 발생: HTTP {response.status_code}"

def extract_corrected_text(html_response):
    """
    HTML 응답에서 교정된 문장을 추출하는 함수.
    """
    soup = BeautifulSoup(html_response, "html.parser")

    # 맞춤법 수정된 문장이 포함된 <td class="tdReplace"> 찾기
    result_divs = soup.find_all("td", {"class": "tdReplace"})
    
    if result_divs:
        corrected_text = " ".join(div.text.strip() for div in result_divs)
        return corrected_text
    else:
        return "맞춤법 검사 결과를 가져올 수 없습니다."

if __name__ == "__main__":
    text = input("검사할 문장을 입력하세요: ")
    corrected_text = check_spelling_nara(text)
    
    print("\n[맞춤법 검사 결과]")
    print(f"원본 문장: {text}")
    print(f"수정된 문장: {corrected_text}")
