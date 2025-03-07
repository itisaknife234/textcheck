import streamlit as st
import requests
import json

def check_spelling(text):
    """ 네이버 맞춤법 검사기를 이용해 맞춤법 검사 수행 """
    url = "http://164.125.7.61/speller/results"
    text = text.replace('\n', '\r\n')  # 개행 문자 변환
    response = requests.post(url, data={"text1": text})
    
    if response.status_code == 200:
        try:
            # 응답 데이터에서 JSON 데이터만 추출
            data = response.text.split("data = [", 1)[-1].rsplit("];", 1)[0]
            data = json.loads(data)

            # 교정된 문장 생성
            corrected_text = text
            for error in data:
                if "candWord" in error and error["candWord"]:  # 수정 가능한 단어만 처리
                    corrected_text = corrected_text.replace(error["orgStr"], error["candWord"].split('|')[0])
            
            return corrected_text, data  # 수정된 문장과 오류 목록 반환
        except Exception as e:
            return None, str(e)
    else:
        return None, "네트워크 오류 발생"

# Streamlit UI 구성
st.title("📝 네이버 맞춤법 검사기")

# 사용자 입력 받기
text_input = st.text_area("📌 맞춤법을 검사할 문장을 입력하세요:")

if st.button("✅ 맞춤법 검사하기"):
    if text_input.strip():
        corrected_text, errors = check_spelling(text_input)
        
        if corrected_text:
            # 결과 출력
            st.subheader("🔹 수정된 문장")
            st.write(corrected_text)

            # 수정된 단어 리스트 출력
            if errors and isinstance(errors, list):
                st.subheader("📌 수정된 단어 목록")
                for error in errors:
                    if "orgStr" in error and "candWord" in error and error["candWord"]:
                        st.write(f"👉 **{error['orgStr']}** → *{error['candWord'].split('|')[0]}*")
        else:
            st.error("❌ 맞춤법 검사 중 오류가 발생했습니다. 다시 시도해주세요.")
    else:
        st.warning("⚠️ 문장을 입력해주세요!")
