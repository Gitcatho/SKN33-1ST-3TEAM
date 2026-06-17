import streamlit as st
import mysql.connector
import pandas as pd
import re

st.set_page_config(page_title="FAQ", page_icon="❓", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }
.page-title { font-size: 1.8rem; font-weight: 700; color: #1B2A4A; margin-bottom: 0.3rem; }
.page-sub { font-size: 0.9rem; color: #888; margin-bottom: 1.5rem; }
mark { background-color: #FFE5B4; padding: 0 2px; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

def highlight_keyword(text, keyword):
    if not keyword:
        return text
    pattern = re.compile(re.escape(keyword), re.IGNORECASE)
    return pattern.sub(lambda m: f"<mark>{m.group()}</mark>", str(text))

def get_conn():
    return mysql.connector.connect(
        host="localhost", user="skn_ai", password="1234", database="recallcardb"
    )

@st.cache_data
def load_faq():
    conn = get_conn()
    df = pd.read_sql("SELECT faq_id, question, answer FROM faq ORDER BY faq_id", conn)
    conn.close()
    return df

# ── 타이틀 ───────────────────────────────────────────────
st.markdown('<div class="page-title">❓ 자동차 리콜 FAQ</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">자동차 리콜에 관한 자주 묻는 질문을 확인하세요</div>', unsafe_allow_html=True)

faq_df = load_faq()
st.caption(f"총 {len(faq_df)}개 FAQ")

keyword = st.text_input("🔍 검색어 입력", placeholder="예: 리콜, 무상수리, 결함")

if keyword:
    faq_df = faq_df[
        faq_df["question"].str.contains(keyword, case=False, na=False) |
        faq_df["answer"].str.contains(keyword, case=False, na=False)
    ]

if faq_df.empty:
    st.warning("조회된 FAQ가 없습니다.")
else:
    for _, row in faq_df.iterrows():
        q = highlight_keyword(row["question"], keyword)
        a = highlight_keyword(row["answer"], keyword)
        with st.expander(f"Q. {row['question']}"):
            st.markdown(f"""
            <div style="line-height:1.8;">
                <p><b>질문</b></p>
                <p>{q}</p>
                <hr>
                <p><b>답변</b></p>
                <p>{a}</p>
            </div>
            """, unsafe_allow_html=True)
