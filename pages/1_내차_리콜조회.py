"""
내 차 리콜조회 페이지.

흐름:  제조사 선택 -> 차명 선택 -> 리콜 이력 표시
"""

import streamlit as st

from database import (
    get_car_detail,
    get_cars,
    get_manufacturers,
    get_recalls,
    render_dummy_banner,
)
from ui import badge, vehicle_card

st.set_page_config(page_title="내 차 리콜조회", page_icon="🔎", layout="wide")

st.title("🔎 내 차 리콜조회")
st.caption("제조사와 차명을 선택하면 해당 차종의 리콜 이력을 보여드립니다.")

render_dummy_banner()


def _name_with_id(df, id_col, name_col):
    """selectbox 용 (id, 표시이름) 매핑 dict 생성."""
    return {int(row[id_col]): row[name_col] for _, row in df.iterrows()}


try:
    # ---- 1. 제조사 목록 -------------------------------------------
    manufacturers = get_manufacturers()
    if manufacturers.empty:
        st.warning("제조사 데이터가 없습니다. `db/dummy_data.sql` 을 먼저 실행하세요.")
        st.stop()

    # ---- 2. 제조사 선택 -------------------------------------------
    mfr_map = _name_with_id(manufacturers, "manufacturer_id", "name")
    mfr_id = st.selectbox(
        "제조사",
        options=list(mfr_map.keys()),
        format_func=lambda x: mfr_map[x],
    )

    # ---- 3. 차명 선택 ---------------------------------------------
    cars = get_cars(mfr_id)
    if cars.empty:
        st.info("해당 제조사로 등록된 차종이 없습니다.")
        st.stop()

    car_map = _name_with_id(cars, "car_id", "model_name")
    car_id = st.selectbox(
        "차명",
        options=list(car_map.keys()),
        format_func=lambda x: car_map[x],
    )

    st.divider()

    # ---- 4. 차량 정보 카드 (식별 패널 + 지표 그리드) --------------
    recalls = get_recalls(car_id)
    detail = get_car_detail(car_id)
    model_name = car_map[car_id]
    maker = detail.iloc[0]["maker"] if not detail.empty else "-"

    has_recall = not recalls.empty
    recall_cnt = len(recalls)
    total_units = int(recalls["리콜대수"].sum()) if has_recall else 0
    latest_date = str(recalls["리콜개시일"].max()) if has_recall else "-"
    top_defect = recalls["결함분류"].mode().iloc[0] if has_recall else "-"

    left, right = st.columns([1.1, 2])
    with left:
        vehicle_card(model_name, maker)
    with right:
        with st.container(border=True):
            status = badge("리콜 대상", "danger") if has_recall else badge("리콜 이력 없음", "success")
            st.markdown(f"**리콜 상태**  {status}", unsafe_allow_html=True)
            g1, g2 = st.columns(2)
            g1.metric("리콜 건수", f"{recall_cnt:,} 건")
            g2.metric("총 리콜 대수", f"{total_units:,} 대")
            g3, g4 = st.columns(2)
            g3.metric("최근 리콜 개시일", latest_date)
            g4.metric("대표 결함분류", top_defect)

    st.divider()

    # ---- 5. 리콜 이력 표시 ----------------------------------------
    if not has_recall:
        st.success(f"✅ **{model_name}** 차종에 등록된 리콜 이력이 없습니다.")
    else:
        st.subheader(f"📋 {model_name} 리콜 이력")

        st.dataframe(
            recalls,
            use_container_width=True,
            hide_index=True,
            column_config={
                "리콜개시일": st.column_config.DateColumn("리콜개시일"),
                "생산시작일": st.column_config.DateColumn("생산시작일"),
                "생산종료일": st.column_config.DateColumn("생산종료일"),
                "리콜대수": st.column_config.NumberColumn("리콜대수", format="%d 대"),
                "리콜사유": st.column_config.TextColumn("리콜사유", width="large"),
            },
        )
        st.caption("※ 리콜 대상 여부가 확인되면 가까운 서비스센터에서 무상 수리를 받으실 수 있습니다. (서비스센터 찾기 페이지 예정)")

except Exception as exc:
    st.error(
        "데이터베이스 조회 중 오류가 발생했습니다. "
        "MySQL 연결 정보와 테이블/데이터 준비 상태를 확인하세요."
    )
    with st.expander("오류 상세"):
        st.code(str(exc))