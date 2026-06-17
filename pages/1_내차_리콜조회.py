"""
내차 리콜조회 - 핵심 페이지
제조사·차명을 선택하면 해당 차종의 리콜 대상 여부와 이력을 보여준다.
"""
import streamlit as st

from components import page_setup, run_query, badge, COLORS

page_setup("내차 리콜조회", "🔎")

# 국산 제조사 판별 키워드(스키마에 국산/수입 구분이 없어 제조사명 기반 휴리스틱).
DOMESTIC_KEYWORDS = (
    "현대", "기아", "제네시스", "한국지엠", "쉐보레", "지엠대우", "대우",
    "르노", "삼성", "쌍용", "케이지모빌리티", "KG모빌리티", "타타대우", "자일",
)


def is_domestic(name: str) -> bool:
    return any(k in name for k in DOMESTIC_KEYWORDS)


# ── 헤더 ─────────────────────────────────────────────────────
st.markdown("# 🔎 내 차 리콜조회")
st.caption("제조사와 차명을 선택하면 해당 차종의 리콜 이력을 보여드립니다.")

try:
    makers = run_query("SELECT manufacturer_id, name FROM manufacturer ORDER BY name")
except Exception as e:
    st.error("데이터베이스에 연결할 수 없습니다. MySQL 실행 및 데이터 적재 상태를 확인하세요.")
    st.exception(e)
    st.stop()

# ── 구분 / 제조사 / 차명 선택 ────────────────────────────────
st.markdown("**구분**")
category = st.radio("구분", ["전체", "국산", "수입"], horizontal=True, label_visibility="collapsed")

if category == "국산":
    makers = makers[makers["name"].apply(is_domestic)]
elif category == "수입":
    makers = makers[~makers["name"].apply(is_domestic)]

if makers.empty:
    st.warning("해당 구분에 등록된 제조사가 없습니다.")
    st.stop()

maker_label = st.selectbox("제조사", makers["name"].tolist())
maker_id = int(makers.loc[makers["name"] == maker_label, "manufacturer_id"].iloc[0])

cars = run_query(
    "SELECT car_id, model_name FROM car WHERE manufacturer_id = :mid ORDER BY model_name",
    {"mid": maker_id},
)
if cars.empty:
    st.warning("해당 제조사에 등록된 차종이 없습니다.")
    st.stop()

car_label = st.selectbox("차명", cars["model_name"].tolist())
car_id = int(cars.loc[cars["model_name"] == car_label, "car_id"].iloc[0])

# ── 리콜 이력 조회 ───────────────────────────────────────────
history = run_query(
    """
    SELECT r.recall_date AS 리콜개시일,
           COALESCE(d.defect_group, '미분류') AS 결함분류,
           r.recall_reason AS 리콜사유,
           r.recall_count AS 리콜대수,
           r.prod_start AS 생산시작일,
           r.prod_end AS 생산종료일
    FROM recall r
    LEFT JOIN defect_category d ON r.defect_id = d.defect_id
    WHERE r.car_id = :cid
    ORDER BY r.recall_date DESC
    """,
    {"cid": car_id},
)

is_target = not history.empty
domestic_label = "국산" if is_domestic(maker_label) else "수입"

st.divider()

# ── 결과: 차량정보 카드 + 리콜 상태 카드 ─────────────────────
left, right = st.columns([1, 1.4])

with left:
    st.markdown(
        f"""
        <div class="car-card">
            <div class="label">🚗 차량 정보</div>
            <div class="pill">{domestic_label}</div>
            <div class="label">{maker_label}</div>
            <div class="model">{car_label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right:
    status_badge = badge("리콜 대상", "red") if is_target else badge("대상 아님", "green")
    st.markdown(f"### 리콜 상태 &nbsp; {status_badge}", unsafe_allow_html=True)

    if is_target:
        total_count = int(history["리콜대수"].sum())
        latest_date = history["리콜개시일"].max()
        top_defect = history["결함분류"].mode()
        top_defect = top_defect.iloc[0] if not top_defect.empty else "미분류"

        c1, c2 = st.columns(2)
        c1.metric("리콜 건수", f"{len(history)} 건")
        c2.metric("총 리콜 대수", f"{total_count:,} 대")
        c3, c4 = st.columns(2)
        c3.metric("최근 리콜 개시일", str(latest_date))
        c4.metric("대표 결함분류", top_defect)
    else:
        st.success("현재 등록된 리콜 이력이 없습니다. 안전한 차량입니다. ✅")

# ── 리콜 이력 테이블 ─────────────────────────────────────────
if is_target:
    st.divider()
    st.markdown(f"### 📋 {car_label} 리콜 이력")
    st.dataframe(
        history,
        use_container_width=True,
        hide_index=True,
        column_config={
            "리콜개시일": st.column_config.DateColumn("리콜개시일", format="YYYY-MM-DD"),
            "생산시작일": st.column_config.DateColumn("생산시작일", format="YYYY-MM-DD"),
            "생산종료일": st.column_config.DateColumn("생산종료일", format="YYYY-MM-DD"),
            "리콜대수": st.column_config.NumberColumn("리콜대수", format="%d 대"),
            "리콜사유": st.column_config.TextColumn("리콜사유", width="large"),
        },
    )
    st.caption("※ 리콜 대상 여부가 확인되면 가까운 서비스센터에서 무상 수리를 받으실 수 있습니다.")

# ── 다음 단계 CTA ────────────────────────────────────────────
st.divider()
st.markdown("#### 다음 단계")
cta1, cta2 = st.columns(2)
with cta1:
    st.page_link("pages/3_관련_뉴스.py", label="📰 이 차종의 리콜 관련 뉴스 보기", icon="➡️")
with cta2:
    st.page_link("pages/2_FAQ.py", label="❓ 리콜·무상수리 자주 묻는 질문", icon="➡️")

# 선택한 차종을 뉴스 페이지에서 활용하도록 세션에 저장.
st.session_state["selected_car_id"] = car_id
st.session_state["selected_car_label"] = f"{maker_label} {car_label}"