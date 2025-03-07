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
            json_data = response.text.split("data = [", 1)[-1].rsplit("];", 1)[0]
            data = json.loads(json_data)

            # 원본 텍스트를 수정된 문장으로 변환
            corrected_text = text
            corrections = []  # 수정된 단어 목록
            
            for error in data:
                if "orgStr" in error and "candWord" in error and error["candWord"]:
                    original_word = error["orgStr"]  # 원래 단어
                    suggested_word = error["candWord"].split('|')[0]  # 첫 번째 추천 단어
                    
                    # 수정된 문장 업데이트
                    corrected_text = corrected_text.replace(original_word, suggested_word)
                    
                    # 수정된 단어 리스트 저장
                    corrections.append((original_word, suggested_word))
            
            return corrected_text, corrections
        except Exception as e:
            return None, f"데이터 처리 오류: {e}"
    else:
        return None, "네트워크 오류 발생"

# Streamlit UI 구성
st.title("📝 네이버 맞춤법 검사기")

# 사용자 입력 받기
text_input = st.text_area("📌 맞춤법을 검사할 문장을 입력하세요:")

if st.button("✅ 맞춤법 검사하기"):
    if text_input.strip():
        corrected_text, corrections = check_spelling(text_input)
        
        if corrected_text:
            # 수정된 문장 출력
            st.subheader("🔹 수정된 문장")
            st.write(corrected_text)

            # 수정된 단어 리스트 출력
            if corrections:
                st.subheader("📌 수정된 단어 목록")
                for original, corrected in corrections:
                    st.write(f"👉 **{original}** → *{corrected}*")
            else:
                st.info("🔍 수정할 단어가 없습니다!")
        else:
            st.error(f"❌ 맞춤법 검사 중 오류가 발생했습니다: {corrections}")
    else:
        st.warning("⚠️ 문장을 입력해주세요!")
