import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

st.set_page_config(page_title="리콜 데이터 분석", layout="wide")
load_dotenv()

PRIMARY   = "#FF6B35"   # 오렌지
SECONDARY = "#1B2A4A"   # 다크블루
LIGHT_PRIMARY = "#FFD0BC"
LIGHT_SECONDARY = "#8FA3C0"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
html, body, [class*="css"] {{ font-family: 'Noto Sans KR', sans-serif; }}
.page-title {{ font-size: 2rem; font-weight: 700; color: {SECONDARY}; margin-bottom: 0.2rem; }}
.page-subtitle {{ font-size: 0.9rem; color: #888; margin-bottom: 1.5rem; }}
.kpi-card {{ background: #f4f6fb; border-radius: 12px; padding: 1.2rem 1.5rem; border-left: 4px solid {PRIMARY}; }}
.kpi-label {{ font-size: 0.78rem; color: #888; font-weight: 500; letter-spacing: 0.05em; text-transform: uppercase; }}
.kpi-value {{ font-size: 1.8rem; font-weight: 700; color: {SECONDARY}; margin-top: 0.2rem; }}
.section-title {{ font-size: 1.1rem; font-weight: 700; color: {SECONDARY}; margin-bottom: 0.3rem; padding-bottom: 0.5rem; border-bottom: 2px solid {PRIMARY}; display: inline-block; }}
.section-caption {{ font-size: 0.82rem; color: #999; margin-bottom: 1rem; }}
.no-data {{ background: #f4f6fb; border-radius: 12px; padding: 2rem; text-align: center; color: #aaa; font-size: 0.95rem; }}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    engine = create_engine(
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT', 3306)}/{os.getenv('DB_NAME')}"
    )
    query = """
        SELECT r.recall_id, r.recall_date, r.recall_count, r.prod_start,
               c.model_name, m.name AS manufacturer
        FROM recall r
        JOIN car c ON r.car_id = c.car_id
        JOIN manufacturer m ON c.manufacturer_id = m.manufacturer_id
    """
    df = pd.read_sql(query, engine)
    df['recall_date'] = pd.to_datetime(df['recall_date'])
    df['prod_start']  = pd.to_datetime(df['prod_start'])
    df['year']        = df['recall_date'].dt.year
    df['prod_year']   = df['prod_start'].dt.year
    return df

@st.cache_data
def load_service():
    engine = create_engine(
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT', 3306)}/{os.getenv('DB_NAME')}"
    )
    query = """
        SELECT m.name AS manufacturer, COUNT(s.center_id) AS center_count
        FROM service_center s
        JOIN manufacturer m ON s.manufacturer_id = m.manufacturer_id
        GROUP BY m.name
    """
    return pd.read_sql(query, engine)

df = load_data()
service_df = load_service()

FONT = dict(family="Noto Sans KR, sans-serif", size=13, color=SECONDARY)
LAYOUT = dict(
    font=FONT, plot_bgcolor="white", paper_bgcolor="white",
    margin=dict(t=20, b=40, l=40, r=80),
    hoverlabel=dict(font_size=13, font_family="Noto Sans KR"),
)

# ── 타이틀 ───────────────────────────────────────────────
st.markdown('<div class="page-title">📊 리콜 데이터 분석</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">국내 자동차 리콜 현황을 한눈에 파악하세요</div>', unsafe_allow_html=True)

# ── 연도 슬라이더 ─────────────────────────────────────────
year_min, year_max = int(df['year'].min()), int(df['year'].max())
year_range = st.slider("📅 리콜 연도 범위", year_min, year_max, (year_min, year_max))
filtered = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

# ── KPI 카드 ──────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
k1, k2, k3, k4 = st.columns(4)
kpi_data = [
    ("총 리콜 건수", f"{len(filtered):,}건"),
    ("총 리콜 대수", f"{filtered['recall_count'].sum():,}대"),
    ("제조사 수",    f"{filtered['manufacturer'].nunique():,}개"),
    ("차종 수",      f"{filtered['model_name'].nunique():,}종"),
]
for col, (label, value) in zip([k1, k2, k3, k4], kpi_data):
    col.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── 차트 1 & 2 ────────────────────────────────────────────
col_a, col_b = st.columns(2)

with col_a:
    st.markdown('<div class="section-title">제조사별 리콜 건수 TOP 10</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-caption">리콜 건수 기준 상위 10개 제조사</div>', unsafe_allow_html=True)
    top10 = filtered.groupby('manufacturer').size().reset_index(name='건수').nlargest(10, '건수').sort_values('건수')
    fig1 = px.bar(top10, x='건수', y='manufacturer', orientation='h', text='건수',
                  color='건수', color_continuous_scale=[[0, LIGHT_PRIMARY], [1, PRIMARY]])
    fig1.update_traces(texttemplate='%{text:,}회', textposition='outside', marker_line_width=0)
    fig1.update_layout(**LAYOUT, height=380, showlegend=False, coloraxis_showscale=False,
                       xaxis=dict(showgrid=True, gridcolor='#f0f0f0', title='',
                                  range=[0, top10['건수'].max() * 1.25]),
                       yaxis=dict(title=''))
    st.plotly_chart(fig1, use_container_width=True)

with col_b:
    st.markdown('<div class="section-title">연도별 리콜 추이</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-caption">리콜 건수 연도별 변화 흐름</div>', unsafe_allow_html=True)
    yearly = filtered.groupby('year').size().reset_index(name='건수')
    fig2 = px.line(yearly, x='year', y='건수', markers=True)
    fig2.update_traces(line_color=PRIMARY, marker_color=PRIMARY,
                       marker_size=7, line_width=2.5,
                       fill='tozeroy', fillcolor='rgba(255,107,53,0.08)')
    fig2.update_layout(**LAYOUT, height=380,
                       xaxis=dict(showgrid=False, title='', dtick=1),
                       yaxis=dict(showgrid=True, gridcolor='#f0f0f0', title=''))
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── 차트 4: 리콜 vs 서비스센터 ───────────────────────────
st.markdown('<div class="section-title">제조사별 리콜 건수 vs 서비스센터 수</div>', unsafe_allow_html=True)
st.markdown('<div class="section-caption">리콜이 많은데 센터가 적은 브랜드는 대응 여력이 부족할 수 있습니다</div>', unsafe_allow_html=True)
recall_by_mfr = filtered.groupby('manufacturer').size().reset_index(name='리콜건수')
merged = recall_by_mfr.merge(service_df, on='manufacturer').nlargest(15, '리콜건수')
fig4 = go.Figure()
fig4.add_trace(go.Bar(
    x=merged['manufacturer'], y=merged['리콜건수'],
    name='리콜 건수', marker_color=PRIMARY, yaxis='y1', marker_line_width=0
))
fig4.add_trace(go.Scatter(
    x=merged['manufacturer'], y=merged['center_count'],
    name='서비스센터 수', mode='lines+markers',
    line=dict(color=SECONDARY, width=2.5),
    marker=dict(color=SECONDARY, size=8), yaxis='y2'
))
fig4.update_layout(
    **LAYOUT, height=400,
    yaxis=dict(title='리콜 건수', showgrid=True, gridcolor='#f0f0f0'),
    yaxis2=dict(title='서비스센터 수', overlaying='y', side='right', showgrid=False),
    legend=dict(orientation='h', y=1.08, x=0, font=dict(size=13)),
    xaxis=dict(showgrid=False)
)
st.plotly_chart(fig4, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── 차트 5: 제조사 선택 → 차종별 ────────────────────────
st.markdown('<div class="section-title">제조사별 차종 리콜 현황</div>', unsafe_allow_html=True)
st.markdown('<div class="section-caption">제조사를 선택하면 해당 브랜드의 차종별 리콜 건수를 확인할 수 있습니다</div>', unsafe_allow_html=True)

valid_manufacturers = (
    filtered.groupby('manufacturer').size()
    .reset_index(name='건수').query('건수 >= 5')
    ['manufacturer'].sort_values().tolist()
)
selected_manufacturer = st.selectbox("🏭 제조사 선택", valid_manufacturers)

car_filtered = filtered[filtered['manufacturer'] == selected_manufacturer]
car_top = car_filtered.groupby('model_name').size().reset_index(name='건수').nlargest(10, '건수').sort_values('건수')

if len(car_top) == 0:
    st.markdown('<div class="no-data">해당 제조사의 리콜 데이터가 없습니다</div>', unsafe_allow_html=True)
else:
    fig5 = px.bar(car_top, x='건수', y='model_name', orientation='h', text='건수',
                  color='건수', color_continuous_scale=[[0, LIGHT_SECONDARY], [1, SECONDARY]])
    fig5.update_traces(texttemplate='%{text:,}회', textposition='outside', marker_line_width=0)
    fig5.update_layout(**LAYOUT, height=max(300, len(car_top) * 45),
                       showlegend=False, coloraxis_showscale=False,
                       xaxis=dict(showgrid=True, gridcolor='#f0f0f0', title='',
                                  range=[0, car_top['건수'].max() * 1.25]),
                       yaxis=dict(title=''))
    st.plotly_chart(fig5, use_container_width=True)
