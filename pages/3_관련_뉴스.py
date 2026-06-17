"""
관련 뉴스 - 차종별 자동차 리콜 뉴스
네이버 뉴스 API로 수집한 리콜 관련 기사를 차종별로 보여준다.
"""
import streamlit as st

from components import page_setup, run_query, COLORS

page_setup("관련 뉴스", "📰")

st.markdown("# 📰 자동차 리콜 관련 뉴스")
st.caption("차종을 선택하면 해당 차종의 리콜 관련 기사를 모아 보여드립니다.")


def render_news(df):
    """뉴스 DataFrame을 링크 카드 목록으로 렌더링한다."""
    if df.empty:
        st.info("해당 조건의 뉴스가 없습니다.")
        return
    for _, row in df.iterrows():
        st.markdown(
            f"""
            <div style="background:#fff;border:1px solid {COLORS['border']};
                        border-radius:10px;padding:.9rem 1.1rem;margin-bottom:.6rem;">
                <a href="{row['news_link']}" target="_blank"
                   style="color:{COLORS['navy']};font-weight:600;text-decoration:none;">
                   🔗 {row['news_title']}
                </a>
            </div>
            """,
            unsafe_allow_html=True,
        )


tab_car, tab_search = st.tabs(["🚗 차종별 보기", "🔍 전체 검색"])

# ── 차종별 보기 ──────────────────────────────────────────────
with tab_car:
    try:
        makers = run_query("SELECT manufacturer_id, name FROM manufacturer ORDER BY name")
    except Exception as e:
        st.error("데이터베이스에 연결할 수 없습니다.")
        st.exception(e)
        st.stop()

    maker_label = st.selectbox("제조사", makers["name"].tolist(), key="news_maker")
    maker_id = int(makers.loc[makers["name"] == maker_label, "manufacturer_id"].iloc[0])

    cars = run_query(
        "SELECT car_id, model_name FROM car WHERE manufacturer_id = :mid ORDER BY model_name",
        {"mid": maker_id},
    )
    if cars.empty:
        st.warning("해당 제조사에 등록된 차종이 없습니다.")
    else:
        # 리콜조회 페이지에서 넘어왔다면 해당 차종을 기본 선택.
        default_idx = 0
        sel_label = st.session_state.get("selected_car_label", "")
        for i, m in enumerate(cars["model_name"].tolist()):
            if sel_label.endswith(m):
                default_idx = i
                break

        car_label = st.selectbox(
            "차명", cars["model_name"].tolist(), index=default_idx, key="news_car"
        )
        car_id = int(cars.loc[cars["model_name"] == car_label, "car_id"].iloc[0])

        news = run_query(
            "SELECT news_title, news_link FROM news WHERE car_id = :cid ORDER BY news_id DESC",
            {"cid": car_id},
        )
        st.write(f"**{maker_label} {car_label}** 관련 뉴스 {len(news)}건")
        render_news(news)

# ── 전체 검색 ────────────────────────────────────────────────
with tab_search:
    keyword = st.text_input("뉴스 제목 검색", placeholder="예: 아이오닉, 에어백, 화재", key="news_kw")
    if keyword:
        news = run_query(
            "SELECT news_title, news_link FROM news "
            "WHERE news_title LIKE :kw ORDER BY news_id DESC LIMIT 100",
            {"kw": f"%{keyword}%"},
        )
        st.write(f"'{keyword}' 검색 결과 {len(news)}건 (최대 100건)")
        render_news(news)
    else:
        st.info("검색어를 입력하세요.")