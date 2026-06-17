"""
FAQ - 자동차 리콜 자주 묻는 질문
"""
import re

import streamlit as st

from components import page_setup, run_query

page_setup("FAQ 조회", "❓")


def highlight_keyword(text: str, keyword: str) -> str:
    """검색어를 <mark>로 감싸 강조한다."""
    if not keyword:
        return str(text)
    pattern = re.compile(re.escape(keyword), re.IGNORECASE)
    return pattern.sub(lambda m: f"<mark>{m.group()}</mark>", str(text))


st.markdown("# ❓ 자동차 리콜 FAQ")
st.caption("리콜 절차, 무상수리 등 자주 묻는 질문을 모았습니다.")

try:
    faq_df = run_query("SELECT faq_id, question, answer FROM faq ORDER BY faq_id")
except Exception as e:
    st.error("FAQ 데이터를 불러오는 중 오류가 발생했습니다.")
    st.exception(e)
    st.stop()

keyword = st.text_input("검색어를 입력하세요", placeholder="예: 리콜, 무상수리, 결함")

if keyword:
    faq_df = faq_df[
        faq_df["question"].str.contains(keyword, case=False, na=False)
        | faq_df["answer"].str.contains(keyword, case=False, na=False)
    ]

st.write(f"총 **{len(faq_df)}개**의 FAQ")

if faq_df.empty:
    st.warning("조회된 FAQ가 없습니다.")
else:
    for _, row in faq_df.iterrows():
        with st.expander(f"Q. {row['question']}"):
            st.markdown(
                f"""
                <div style="line-height:1.8;">
                    <p><b>질문</b></p>
                    <p>{highlight_keyword(row['question'], keyword)}</p>
                    <hr>
                    <p><b>답변</b></p>
                    <p>{highlight_keyword(row['answer'], keyword)}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )