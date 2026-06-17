"""
RecallChecker - 홈(랜딩) 페이지
내 차가 리콜 대상인지 한눈에 확인하는 자동차 리콜 정보 서비스.
한국교통안전공단 리콜 데이터 기반.
"""
import streamlit as st

from components import page_setup, run_query, feature_card, COLORS

page_setup("RecallChecker - 내차 리콜조회", "🚗")

# ── 상단 브랜드 ──────────────────────────────────────────────
st.markdown(
    f"<h2 style='color:{COLORS['navy']};margin-bottom:1.2rem'>🚗 RecallChecker</h2>",
    unsafe_allow_html=True,
)

# ── Hero 배너 ────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero">
        <span class="tag">🛡️ 한국교통안전공단 리콜 데이터 기반</span>
        <h1>내 차, 리콜 대상인가요?<br>지금 바로 확인하세요</h1>
        <p>제작사와 차명만 선택하면 리콜 대상 여부를 즉시 알려드립니다.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")
st.page_link("pages/1_내차_리콜조회.py", label="🔎 리콜 대상 조회하기", icon="➡️")

# ── 기능 카드 4분할 ──────────────────────────────────────────
st.write("")
cards = [
    ("🔎", "간편한 조회", "제작사, 차명만 선택하면 리콜 해당 여부를 바로 확인할 수 있어요."),
    ("📋", "리콜 사유 안내", "어떤 결함으로 리콜이 실시됐는지 상세 사유를 제공합니다."),
    ("📊", "브랜드별 분석", "어떤 브랜드와 차종에 리콜이 많은지 데이터로 분석해 드립니다."),
    ("🛡️", "공식 데이터", "한국교통안전공단의 공식 리콜 현황 데이터를 기반으로 합니다."),
]
for col, (icon, title, desc) in zip(st.columns(4), cards):
    col.markdown(feature_card(icon, title, desc), unsafe_allow_html=True)

# ── 통계 지표 ────────────────────────────────────────────────
st.write("")
st.write("")


@st.cache_data(ttl=600, show_spinner=False)
def load_stats():
    recall_cnt = run_query("SELECT COUNT(*) AS c FROM recall")["c"][0]
    car_cnt = run_query("SELECT COUNT(*) AS c FROM car")["c"][0]
    maker_cnt = run_query("SELECT COUNT(*) AS c FROM manufacturer")["c"][0]
    return int(recall_cnt), int(car_cnt), int(maker_cnt)


try:
    recall_cnt, car_cnt, maker_cnt = load_stats()
    m1, m2, m3 = st.columns(3)
    m1.metric("누적 리콜 건수", f"{recall_cnt:,}")
    m2.metric("등록 차종", f"{car_cnt:,}")
    m3.metric("등록 제조사", f"{maker_cnt:,}")
except Exception as e:
    st.error("데이터베이스에 연결할 수 없습니다. MySQL 실행 및 데이터 적재 상태를 확인하세요.")
    st.exception(e)

# ── 다크 CTA 배너 ────────────────────────────────────────────
st.markdown(
    """
    <div class="cta-banner">
        <h3>내 차의 안전을 지금 확인하세요</h3>
        <p>리콜을 모르고 지나치면 안전에 위협이 될 수 있습니다.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.write("")
st.page_link("pages/1_내차_리콜조회.py", label="🚗 리콜 조회 시작하기", icon="➡️")