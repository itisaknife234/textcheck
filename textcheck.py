import streamlit as st
import requests
from bs4 import BeautifulSoup

def check_spelling(text):
    """ 네이버 맞춤법 검사기를 이용해 맞춤법 검사 수행 """
    url = "http://164.125.7.61/speller/results"
    data = {"text1": text}
    
    # 맞춤법 검사 요청
    response = requests.post(url, data=data)
    
    if response.status_code == 200:
        # HTML 파싱
        soup = BeautifulSoup(response.text, "html.parser")
        # 결과 추출 (수정된 문장 가져오기)
        corrected_text = soup.find("td", class_="tdReplace").text.strip()
        return corrected_text
    else:
        return None

# Streamlit UI 구성
st.title("📝 네이버 맞춤법 검사기")

# 사용자 입력 받기
text_input = st.text_area("📌 맞춤법을 검사할 문장을 입력하세요:")

if st.button("✅ 맞춤법 검사하기"):
    if text_input.strip():
        corrected_text = check_spelling(text_input)
        
        if corrected_text:
            # 결과 출력
            st.subheader("🔹 수정된 문장")
            st.write(corrected_text)
        else:
            st.error("❌ 맞춤법 검사 중 오류가 발생했습니다. 다시 시도해주세요.")
    else:
        st.warning("⚠️ 문장을 입력해주세요!")
