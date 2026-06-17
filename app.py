import streamlit as st

st.set_page_config(
    page_title="자동차 리콜 서비스",
    page_icon="🚗",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }

.hero {
    background: linear-gradient(135deg, #1B2A4A 0%, #2d4270 100%);
    border-radius: 16px;
    padding: 3rem 2.5rem;
    color: white;
    margin-bottom: 2rem;
}
.hero-title {
    font-size: 2.4rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}
.hero-sub {
    font-size: 1rem;
    opacity: 0.8;
    margin-bottom: 1.5rem;
}
.card {
    background: #f8f9fc;
    border-radius: 12px;
    padding: 1.5rem;
    border-top: 4px solid #FF6B35;
    height: 100%;
}
.card-icon { font-size: 2rem; margin-bottom: 0.5rem; }
.card-title { font-size: 1rem; font-weight: 700; color: #1B2A4A; margin-bottom: 0.3rem; }
.card-desc { font-size: 0.85rem; color: #888; }
</style>
""", unsafe_allow_html=True)

# ── 히어로 섹션 ───────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-title">🚗 자동차 리콜 서비스</div>
    <div class="hero-sub">내 차의 리콜 여부를 확인하고, 가까운 서비스센터를 찾아보세요</div>
</div>
""", unsafe_allow_html=True)

# ── 바로가기 버튼 ─────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="card">
        <div class="card-icon">🔍</div>
        <div class="card-title">내 차 리콜 조회</div>
        <div class="card-desc">브랜드와 차종을 선택해 리콜 대상 여부를 확인하세요</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("리콜 조회하기", use_container_width=True, type="primary"):
        st.switch_page("pages/1_recall.py")

with col2:
    st.markdown("""
    <div class="card">
        <div class="card-icon">📊</div>
        <div class="card-title">리콜 데이터 분석</div>
        <div class="card-desc">제조사별, 연도별 리콜 현황을 한눈에 파악하세요</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("분석 보기", use_container_width=True):
        st.switch_page("pages/2_analysis.py")

with col3:
    st.markdown("""
    <div class="card">
        <div class="card-icon">📍</div>
        <div class="card-title">서비스센터 찾기</div>
        <div class="card-desc">내 지역 근처 서비스센터 위치와 연락처를 확인하세요</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("센터 찾기", use_container_width=True):
        st.switch_page("pages/3_service_center.py")

with col4:
    st.markdown("""
    <div class="card">
        <div class="card-icon">📰</div>
        <div class="card-title">리콜 뉴스</div>
        <div class="card-desc">최신 자동차 리콜 관련 뉴스를 확인하세요</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("뉴스 보기", use_container_width=True):
        st.switch_page("pages/4_news.py")