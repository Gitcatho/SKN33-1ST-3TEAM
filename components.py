"""
공통 헬퍼 모듈
- DB 연결 / 쿼리 (캐시 적용)
- 디자인 시스템(컬러 팔레트) 및 전역 CSS
- 공통 UI 컴포넌트(헤더, 배지, 지표 카드 등)

모든 페이지(app.py, pages/*.py)에서 import 하여 사용한다.
"""
import os
from pathlib import Path

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# ── 환경변수 로드 ────────────────────────────────────────────
load_dotenv(Path(__file__).resolve().parent / ".env")

DB_USER = os.getenv("DB_USER", "skn_ai")
DB_PASSWORD = os.getenv("DB_PASSWORD", "1234")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_NAME = os.getenv("DB_NAME", "recallcardb")


# ── 디자인 시스템: 컬러 팔레트 ───────────────────────────────
COLORS = {
    "navy": "#1B2A4A",      # 신뢰 - 차량정보 카드/강조 배너
    "red": "#E8412C",       # 경고/주목 - Hero, '리콜 대상' 배지
    "red_dark": "#C5301E",
    "green": "#2E9E5B",     # 안전 - '대상 아님' 배지
    "yellow_bg": "#FFF8E1",  # 안내 배너 배경
    "yellow_bd": "#F1D592",
    "gray_bg": "#F5F7FA",
    "gray_text": "#5B6472",
    "border": "#E3E8EF",
}


# ── DB 연결 / 쿼리 ───────────────────────────────────────────
@st.cache_resource
def get_engine():
    """SQLAlchemy 엔진을 생성한다(앱 전역에서 1회 재사용)."""
    url = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
    )
    return create_engine(url, pool_pre_ping=True)


@st.cache_data(ttl=600, show_spinner=False)
def run_query(sql: str, params: dict | None = None) -> pd.DataFrame:
    """SELECT 쿼리를 실행해 DataFrame으로 반환한다(10분 캐시)."""
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql(text(sql), conn, params=params or {})


# ── 전역 CSS ─────────────────────────────────────────────────
def inject_css():
    """모든 페이지 상단에서 호출. 디자인 시스템 CSS를 주입한다."""
    st.markdown(
        f"""
        <style>
            .stApp {{ background: {COLORS['gray_bg']}; }}
            .block-container {{ padding-top: 2.5rem; max-width: 1100px; }}

            /* Hero 배너 */
            .hero {{
                background: linear-gradient(135deg, {COLORS['red']} 0%, {COLORS['red_dark']} 100%);
                color: #fff; border-radius: 18px; padding: 3rem 2rem;
                text-align: center; box-shadow: 0 10px 30px rgba(232,65,44,.25);
            }}
            .hero .tag {{
                display: inline-block; background: rgba(255,255,255,.2);
                padding: .35rem 1rem; border-radius: 999px;
                font-size: .85rem; margin-bottom: 1rem;
            }}
            .hero h1 {{ color:#fff; font-size: 2.4rem; line-height: 1.3; margin: 0; }}
            .hero p {{ color: rgba(255,255,255,.92); margin-top: 1rem; font-size: 1.05rem; }}

            /* 기능 카드 */
            .feature-card {{
                background:#fff; border:1px solid {COLORS['border']};
                border-radius:14px; padding:1.5rem; height:100%;
                box-shadow:0 2px 8px rgba(0,0,0,.03);
            }}
            .feature-card .icon {{ font-size:1.8rem; }}
            .feature-card h4 {{ margin:.6rem 0 .4rem; color:{COLORS['navy']}; }}
            .feature-card p {{ color:{COLORS['gray_text']}; font-size:.9rem; margin:0; line-height:1.6; }}

            /* 안내(노란) 배너 */
            .notice {{
                background:{COLORS['yellow_bg']}; border:1px solid {COLORS['yellow_bd']};
                border-radius:12px; padding:1rem 1.25rem; color:#7a5d00; font-size:.92rem;
            }}

            /* 차량정보(네이비) 카드 */
            .car-card {{
                background: linear-gradient(135deg, {COLORS['navy']} 0%, #2C3E63 100%);
                color:#fff; border-radius:16px; padding:1.5rem;
            }}
            .car-card .label {{ opacity:.8; font-size:.9rem; }}
            .car-card .pill {{
                display:inline-block; background:rgba(255,255,255,.18);
                padding:.2rem .8rem; border-radius:999px; font-size:.8rem; margin:.5rem 0;
            }}
            .car-card .model {{
                background:#fff; color:{COLORS['navy']}; border:2px solid #F5A623;
                border-radius:10px; padding:.9rem; text-align:center;
                font-weight:700; font-size:1.1rem; margin-top:.6rem;
            }}

            /* 상태 배지 */
            .badge {{
                display:inline-block; padding:.25rem .9rem; border-radius:999px;
                font-weight:700; font-size:.9rem; color:#fff;
            }}
            .badge-red {{ background:{COLORS['red']}; }}
            .badge-green {{ background:{COLORS['green']}; }}

            /* 다크 CTA 배너 */
            .cta-banner {{
                background:{COLORS['navy']}; color:#fff; border-radius:16px;
                padding:2.5rem; text-align:center; margin-top:1.5rem;
            }}
            .cta-banner h3 {{ color:#fff; margin:0; font-size:1.6rem; }}
            .cta-banner p {{ color:rgba(255,255,255,.8); margin-top:.6rem; }}

            mark {{ background:#FFE8A3; padding:0 .15rem; border-radius:3px; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ── 공통 컴포넌트 ────────────────────────────────────────────
def page_setup(title: str, icon: str):
    """페이지 공통 초기화: set_page_config + CSS 주입."""
    st.set_page_config(page_title=title, page_icon=icon, layout="wide")
    inject_css()


def badge(text: str, kind: str = "red") -> str:
    """상태 배지 HTML 문자열을 반환한다. kind: 'red' | 'green'"""
    return f'<span class="badge badge-{kind}">{text}</span>'


def feature_card(icon: str, title: str, desc: str) -> str:
    """홈 기능 카드 HTML 문자열."""
    return (
        f'<div class="feature-card"><div class="icon">{icon}</div>'
        f'<h4>{title}</h4><p>{desc}</p></div>'
    )