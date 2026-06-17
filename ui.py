"""
공통 UI 헬퍼 - 페이지 간 디자인 일관성 유지.

Streamlit 네이티브 + 절제된 st.html 만 사용 (버전 안정성 우선).
색상 상수는 .streamlit/config.toml 테마와 동일하게 유지하세요.
"""

import streamlit as st

# ---- 테마 색상 (config.toml 과 일치) --------------------------------
PRIMARY = "#D32F2F"   # 레드 (리콜/안전 포인트)
PRIMARY_DARK = "#B71C1C"
DARK = "#0F1B2D"      # 다크 네이비 (CTA 배너)
DANGER = "#C62828"    # 리콜 대상/위험
WARNING = "#F9A825"   # 주의/더미
SUCCESS = "#2E7D32"   # 정상/완료
MUTED = "#5F6B7A"     # 보조 텍스트

_BADGE_COLORS = {
    "danger": DANGER,
    "warning": WARNING,
    "success": SUCCESS,
    "info": PRIMARY,
}


def badge(text: str, kind: str = "info") -> str:
    """인라인 배지 HTML 문자열을 반환. st.markdown(..., unsafe_allow_html=True) 로 출력.

    kind: "danger" | "warning" | "success" | "info"
    """
    color = _BADGE_COLORS.get(kind, PRIMARY)
    return (
        f"<span style='background:{color};color:#fff;padding:2px 10px;"
        f"border-radius:12px;font-size:0.8rem;font-weight:600;"
        f"white-space:nowrap;'>{text}</span>"
    )


def hero(title: str, subtitle: str = "", kicker: str = "") -> None:
    """중앙 정렬 히어로 배너 (레드 그라데이션). kicker 는 상단 알약형 라벨."""
    kicker_html = (
        f"<div style='display:inline-block;background:rgba(255,255,255,.18);"
        f"color:#fff;padding:4px 14px;border-radius:20px;font-size:.85rem;"
        f"font-weight:600;margin-bottom:1rem;'>{kicker}</div>"
        if kicker else ""
    )
    sub_html = (
        f"<p style='margin:1rem 0 0;font-size:1.05rem;opacity:.92;'>{subtitle}</p>"
        if subtitle else ""
    )
    st.html(
        f"""
        <div style="background:linear-gradient(135deg,#E53935,{PRIMARY_DARK});
                    padding:3rem 2rem;border-radius:16px;color:#fff;
                    text-align:center;margin-bottom:1.4rem;">
            {kicker_html}
            <h1 style="margin:0;font-size:2.3rem;font-weight:800;line-height:1.3;">{title}</h1>
            {sub_html}
        </div>
        """
    )


def cta_banner(title: str, subtitle: str = "") -> None:
    """다크 네이비 CTA 배너 (중앙 정렬)."""
    sub_html = (
        f"<p style='margin:.8rem 0 0;font-size:1rem;opacity:.85;'>{subtitle}</p>"
        if subtitle else ""
    )
    st.html(
        f"""
        <div style="background:{DARK};padding:2.6rem 2rem;border-radius:16px;
                    color:#fff;text-align:center;margin:1rem 0 1.2rem;">
            <h2 style="margin:0;font-size:1.6rem;font-weight:700;">{title}</h2>
            {sub_html}
        </div>
        """
    )


def vehicle_card(model_name: str, maker: str, country: str) -> None:
    """차량 식별 패널 (자동차365 스타일). 번호판 자리에는 차명을 표기."""
    st.html(
        f"""
        <div style="background:linear-gradient(135deg,#1B3A6B,{DARK});
                    padding:1.4rem 1.5rem;border-radius:14px;color:#fff;height:100%;">
            <div style="font-size:.82rem;opacity:.85;margin-bottom:.6rem;">🚗 차량 정보</div>
            <span style="display:inline-block;background:rgba(255,255,255,.18);
                         padding:2px 12px;border-radius:14px;font-size:.8rem;
                         font-weight:600;">{country}</span>
            <div style="margin:.7rem 0 .2rem;font-size:.85rem;opacity:.85;">{maker}</div>
            <div style="background:#fff;color:{DARK};border:3px solid #FFC107;
                        border-radius:10px;padding:.7rem;text-align:center;
                        font-weight:800;font-size:1.25rem;margin-top:.4rem;">
                {model_name}
            </div>
        </div>
        """
    )


def feature_card(col, icon: str, title: str, desc: str) -> None:
    """피처 카드 한 장을 주어진 컬럼에 렌더링."""
    with col:
        with st.container(border=True):
            st.markdown(f"## {icon}")
            st.markdown(f"**{title}**")
            st.caption(desc)


def section_header(title: str, subtitle: str = "") -> None:
    """섹션 제목 + 설명."""
    st.subheader(title)
    if subtitle:
        st.caption(subtitle)