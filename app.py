"""
자동차 리콜 정보 조회 서비스 - 랜딩(홈) 페이지.

실행:  streamlit run app.py
사전 준비:
    1) db/init.sql                실행 (계정/스키마/테이블)
    2) db/recallcardb_script.sql  실행 (테이블 생성)
    3) db/dummy_data.sql          실행 (시연용 더미 데이터)
"""

import streamlit as st

from database import render_dummy_banner, run_query
from ui import cta_banner, feature_card, hero

# 랜딩은 사이드바를 접은 상태로 시작 (사용자가 좌측 » 화살표로 다시 열 수 있음)
st.set_page_config(
    page_title="자동차 리콜 조회",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

RECALL_PAGE = "pages/1_내차_리콜조회.py"

# ---- 상단 가로 네비게이션 (비고정) ----------------------------------
nav = st.columns([3, 1, 1, 1, 1, 1.2])
nav[0].markdown("### 🚗 RecallChecker")
nav[1].page_link("app.py", label="홈", icon="🏠")
nav[2].page_link(RECALL_PAGE, label="리콜 조회", icon="🔎")
nav[3].page_link(RECALL_PAGE, label="리콜 분석", icon="📊", disabled=True)
nav[4].page_link(RECALL_PAGE, label="FAQ", icon="❓", disabled=True)
nav[5].page_link(RECALL_PAGE, label="결함신고", icon="🚨", disabled=True)

st.divider()

# ---- 히어로 ---------------------------------------------------------
hero(
    title="내 차, 리콜 대상인가요?<br>지금 바로 확인하세요",
    subtitle="제작사와 차명, 생산연도만 입력하면 리콜 대상 여부를 즉시 알려드립니다.",
    kicker="🛡️ 한국교통안전공단 리콜 데이터 기반",
)

# 히어로 바로 아래 1차 CTA
st.page_link(RECALL_PAGE, label="🔎 리콜 대상 조회하기 →")

render_dummy_banner()

st.write("")

# ---- 피처 카드 ------------------------------------------------------
cols = st.columns(4)
feature_card(cols[0], "🔎", "간편한 조회",
             "제작사, 차명, 생산연도만 입력하면 리콜 해당 여부를 바로 확인할 수 있어요.")
feature_card(cols[1], "📋", "리콜 사유 안내",
             "어떤 결함으로 리콜이 실시됐는지 상세 사유를 제공합니다.")
feature_card(cols[2], "📊", "브랜드별 분석",
             "어떤 브랜드와 차종에 리콜이 많은지 데이터로 분석해 드립니다.")
feature_card(cols[3], "🛡️", "공식 데이터",
             "한국교통안전공단의 공식 리콜 현황 데이터를 기반으로 합니다.")

# ---- 요약 통계 ------------------------------------------------------
@st.cache_data(ttl=600, show_spinner=False)
def _load_summary() -> dict:
    counts = {}
    for label, table in [("리콜", "recall"), ("차종", "car"), ("제조사", "manufacturer")]:
        df = run_query(f"SELECT COUNT(*) AS c FROM {table}")
        counts[label] = int(df.iloc[0, 0]) if not df.empty else 0
    return counts


st.write("")
try:
    summary = _load_summary()
    c1, c2, c3 = st.columns(3)
    c1.metric("누적 리콜 건수", f"{summary['리콜']:,}")
    c2.metric("등록 차종", f"{summary['차종']:,}")
    c3.metric("등록 제조사", f"{summary['제조사']:,}")
except Exception as exc:
    st.error(
        "데이터베이스에 연결하지 못했습니다. "
        "MySQL 실행 여부와 연결 정보를 확인하세요.\n\n"
        "준비 순서: `db/init.sql` → `db/recallcardb_script.sql` → `db/dummy_data.sql`"
    )
    with st.expander("오류 상세"):
        st.code(str(exc))

# ---- 하단 다크 CTA --------------------------------------------------
cta_banner(
    "내 차의 안전을 지금 확인하세요",
    "리콜을 모르고 지나치면 안전에 위협이 될 수 있습니다.",
)
st.page_link(RECALL_PAGE, label="🚗 리콜 조회 시작하기 →")