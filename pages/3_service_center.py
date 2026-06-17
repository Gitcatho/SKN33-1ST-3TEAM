import streamlit as st
import mysql.connector
import pandas as pd

st.set_page_config(page_title="서비스센터 찾기", page_icon="📍", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }
.page-title { font-size: 1.8rem; font-weight: 700; color: #1B2A4A; margin-bottom: 0.3rem; }
.page-sub { font-size: 0.9rem; color: #888; margin-bottom: 1.5rem; }
.center-card {
    background: #f8f9fc;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin: 0.4rem 0;
    border-left: 4px solid #FF6B35;
}
.center-name { font-size: 0.95rem; font-weight: 700; color: #1B2A4A; }
.center-info { font-size: 0.82rem; color: #666; margin-top: 0.3rem; }
</style>
""", unsafe_allow_html=True)

def get_conn():
    return mysql.connector.connect(
        host="localhost", user="skn_ai", password="1234", database="recallcardb"
    )

@st.cache_data
def load_regions():
    conn = get_conn()
    df = pd.read_sql("SELECT region_id, city, district FROM region ORDER BY city, district", conn)
    conn.close()
    return df

def load_manufacturers_by_region(region_id):
    conn = get_conn()
    df = pd.read_sql(f"""
        SELECT DISTINCT m.manufacturer_id, m.name
        FROM service_center s
        JOIN manufacturer m ON s.manufacturer_id = m.manufacturer_id
        WHERE s.region_id = {region_id}
        ORDER BY m.name
    """, conn)
    conn.close()
    return df

def load_centers(region_id, manufacturer_id=None):
    conn = get_conn()
    query = f"""
        SELECT s.center_name, s.address, s.phone, s.latitude, s.longitude, m.name AS manufacturer
        FROM service_center s
        JOIN manufacturer m ON s.manufacturer_id = m.manufacturer_id
        WHERE s.region_id = {region_id}
    """
    if manufacturer_id:
        query += f" AND s.manufacturer_id = {manufacturer_id}"
    query += " ORDER BY m.name, s.center_name"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# ── 타이틀 ───────────────────────────────────────────────
st.markdown('<div class="page-title">📍 가까운 서비스센터 찾기</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">지역을 선택하면 해당 지역의 서비스센터를 지도와 목록으로 확인할 수 있습니다</div>', unsafe_allow_html=True)

regions = load_regions()

# ── 필터 ─────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)

with col1:
    cities = sorted(regions['city'].unique().tolist())
    selected_city = st.selectbox("🏙️ 시/도 선택", cities, index=None, placeholder="시/도를 선택하세요")

selected_district = None
with col2:
    if selected_city:
        districts = sorted(regions[regions['city'] == selected_city]['district'].tolist())
        selected_district = st.selectbox("🏘️ 구/군 선택", districts, index=None, placeholder="구/군을 선택하세요")
    else:
        st.selectbox("🏘️ 구/군 선택", [], placeholder="시/도를 먼저 선택하세요", disabled=True)

# 지역 선택되면 해당 지역 제조사만 로드
selected_mfr = None
region_id = None
with col3:
    if selected_city and selected_district:
        region_id = int(regions[
            (regions['city'] == selected_city) &
            (regions['district'] == selected_district)
        ]['region_id'].values[0])
        mfr_in_region = load_manufacturers_by_region(region_id)
        mfr_options = ["전체"] + mfr_in_region['name'].tolist()
        selected_mfr = st.selectbox("🏭 제조사 필터 (선택)", mfr_options)
    else:
        st.selectbox("🏭 제조사 필터 (선택)", ["전체"], disabled=True)

# ── 결과 ─────────────────────────────────────────────────
if selected_city and selected_district and region_id:
    mfr_id = None
    if selected_mfr and selected_mfr != "전체":
        mfr_in_region = load_manufacturers_by_region(region_id)
        mfr_id = int(mfr_in_region[mfr_in_region['name'] == selected_mfr]['manufacturer_id'].values[0])

    centers = load_centers(region_id, mfr_id)

    st.markdown(f"<br>**{selected_city} {selected_district}** 서비스센터 **{len(centers)}개**", unsafe_allow_html=True)

    if len(centers) == 0:
        st.info("해당 지역에 서비스센터가 없습니다.")
    else:
        map_data = centers.dropna(subset=['latitude', 'longitude'])[['latitude', 'longitude']]
        if len(map_data) > 0:
            st.map(map_data, zoom=12)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 서비스센터 목록")
        for _, row in centers.iterrows():
            phone_display = row['phone'] if row['phone'] else "전화번호 없음"
            address_display = row['address'] if row['address'] else "주소 없음"
            name_display = row['center_name'] if row['center_name'] else "센터명 없음"
            st.markdown(f"""
            <div class="center-card">
                <div class="center-name">🔧 {name_display}</div>
                <div class="center-info">
                    🏭 {row['manufacturer']} &nbsp;|&nbsp;
                    📌 {address_display} &nbsp;|&nbsp;
                    📞 {phone_display}
                </div>
            </div>
            """, unsafe_allow_html=True)