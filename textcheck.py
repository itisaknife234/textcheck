import streamlit as st
from hanspell import spell_checker

# Streamlit 앱 제목
st.title("📝 맞춤법 검사기")

# 사용자 입력 받기
text_input = st.text_area("📌 맞춤법을 검사할 문장을 입력하세요:")

if st.button("✅ 맞춤법 검사하기"):
    if text_input.strip():
        result = spell_checker.check(text_input)
        checked_text = result.checked  # 수정된 문장
        errors = result.errors         # 틀린 단어 개수
        original_text = result.org     # 원본 문장

        # 결과 출력
        st.subheader("🔹 수정된 문장")
        st.write(checked_text)

        # 틀린 단어 개수 출력
        st.subheader("📌 수정된 단어 개수")
        st.write(f"총 {errors}개의 단어가 수정되었습니다.")

        # 원본 문장과 비교
        st.subheader("🧐 원본 문장과 비교")
        st.write(original_text)
    else:
        st.warning("⚠️ 문장을 입력해주세요!")
