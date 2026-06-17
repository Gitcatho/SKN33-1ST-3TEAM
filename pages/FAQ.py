import streamlit as st
import mysql.connector
import pandas as pd
import re

def highlight_keyword(text, keyword):
    if not keyword:
        return text

    pattern = re.compile(re.escape(keyword), re.IGNORECASE)
    return pattern.sub(lambda m: f"<mark>{m.group()}</mark>", str(text))

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="skn_ai",
        password="1234",
        database="recallcardb"
    )


def load_faq_data():
    conn = get_connection()

    sql = """
        SELECT
            faq_id,
            question,
            answer
        FROM faq
        ORDER BY faq_id
    """

    df = pd.read_sql(sql, conn)
    conn.close()

    return df


st.set_page_config(
    page_title="FAQ 조회",
    page_icon="❓",
    layout="wide"
)

st.title("❓ 자동차 리콜 FAQ")

try:
    faq_df = load_faq_data()

    st.write(f"총 FAQ 개수: {len(faq_df)}개")

    keyword = st.text_input("검색어를 입력하세요", placeholder="예: 리콜, 무상수리, 결함")

    if keyword:
        faq_df = faq_df[
            faq_df["question"].str.contains(keyword, case=False, na=False) |
            faq_df["answer"].str.contains(keyword, case=False, na=False)
        ]

    if faq_df.empty:
        st.warning("조회된 FAQ가 없습니다.")
    else:
        for _, row in faq_df.iterrows():
            highlighted_question = highlight_keyword(row["question"], keyword)
            highlighted_answer = highlight_keyword(row["answer"], keyword)

            with st.expander(f"Q. {row['question']}"):
                st.markdown(
                    f"""
                    <div style="line-height:1.8;">
                        <p><b>질문</b></p>
                        <p>{highlighted_question}</p>
                        <hr>
                        <p><b>답변</b></p>
                        <p>{highlighted_answer}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

except Exception as e:
    st.error("FAQ 데이터를 불러오는 중 오류가 발생했습니다.")
    st.exception(e)