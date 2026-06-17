"""
recallcardb (MySQL) 연결 및 공통 쿼리 모듈.

연결 정보 우선순위:  st.secrets["mysql"]  >  환경변수(MYSQL_*)  >  기본값
기본값은 db/init.sql 에서 만든 계정/스키마(skn_ai / 1234 / recallcardb) 입니다.

st.secrets 사용 예 (.streamlit/secrets.toml):
    [mysql]
    host = "localhost"
    port = "3306"
    user = "skn_ai"
    password = "1234"
    database = "recallcardb"
"""

import os

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text

# 더미 데이터 식별 기준값: PK 가 이 값 이상이면 더미로 간주한다.
DUMMY_ID_THRESHOLD = 9000

_DEFAULTS = {
    "host": "localhost",
    "port": "3306",
    "user": "skn_ai",
    "password": "1234",
    "database": "recallcardb",
}


def _get_config() -> dict:
    try:
        secrets = dict(st.secrets.get("mysql", {}))
    except Exception:
        secrets = {}

    cfg = {}
    for key, default in _DEFAULTS.items():
        cfg[key] = str(
            secrets.get(key)
            or os.getenv(f"MYSQL_{key.upper()}")
            or default
        )
    return cfg


@st.cache_resource(show_spinner=False)
def get_engine():
    cfg = _get_config()
    url = (
        f"mysql+pymysql://{cfg['user']}:{cfg['password']}"
        f"@{cfg['host']}:{cfg['port']}/{cfg['database']}?charset=utf8mb4"
    )
    return create_engine(url, pool_pre_ping=True)


@st.cache_data(ttl=600, show_spinner=False)
def run_query(sql: str, params: dict | None = None) -> pd.DataFrame:
    """SELECT 결과를 DataFrame 으로 반환."""
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql(text(sql), conn, params=params or {})


# ---------------------------------------------------------------------
#  도메인 조회 함수
# ---------------------------------------------------------------------
def get_manufacturers(country: str | None = None) -> pd.DataFrame:
    """제조사 목록. country='국산'/'수입' 으로 필터 가능."""
    sql = "SELECT manufacturer_id, name, country FROM manufacturer"
    params = {}
    if country:
        sql += " WHERE country = :country"
        params["country"] = country
    sql += " ORDER BY name"
    return run_query(sql, params)


def get_cars(manufacturer_id: int) -> pd.DataFrame:
    """특정 제조사의 차량 목록."""
    sql = """
        SELECT car_id, model_name
        FROM car
        WHERE manufacturer_id = :mid
        ORDER BY model_name
    """
    return run_query(sql, {"mid": manufacturer_id})


def get_car_detail(car_id: int) -> pd.DataFrame:
    """차량 1건의 상세(제조사명·국산/수입 포함)."""
    sql = """
        SELECT c.car_id, c.model_name, m.name AS maker, m.country
        FROM car c
        JOIN manufacturer m ON c.manufacturer_id = m.manufacturer_id
        WHERE c.car_id = :car_id
    """
    return run_query(sql, {"car_id": car_id})


def get_recalls(car_id: int) -> pd.DataFrame:
    """특정 차량의 리콜 이력(결함 대분류 조인)."""
    sql = """
        SELECT
            r.recall_date   AS 리콜개시일,
            d.defect_group  AS 결함분류,
            r.recall_reason AS 리콜사유,
            r.recall_count  AS 리콜대수,
            r.prod_start    AS 생산시작일,
            r.prod_end      AS 생산종료일
        FROM recall r
        JOIN defect_category d ON r.defect_id = d.defect_id
        WHERE r.car_id = :car_id
        ORDER BY r.recall_date DESC
    """
    return run_query(sql, {"car_id": car_id})


def has_dummy_data() -> bool:
    """더미 데이터(PK >= 9000)가 한 건이라도 있으면 True."""
    sql = """
        SELECT EXISTS(
            SELECT 1 FROM manufacturer WHERE manufacturer_id >= :t
            UNION ALL
            SELECT 1 FROM recall       WHERE recall_id       >= :t
        ) AS has_dummy
    """
    df = run_query(sql, {"t": DUMMY_ID_THRESHOLD})
    return bool(df.iloc[0, 0]) if not df.empty else False


def render_dummy_banner() -> None:
    """더미 데이터가 섞여 있으면 화면 상단에 경고 배너를 표시."""
    try:
        if has_dummy_data():
            st.warning(
                "⚠️ 현재 **더미(DUMMY) 데이터**가 포함되어 있습니다 "
                "(이름에 `[DUMMY]` 표시 / PK 9000번 이상). "
                "실제 데이터로 교체하려면 `db/dummy_data_remove.sql` 을 실행하세요.",
                icon="⚠️",
            )
    except Exception:
        # 연결 실패 시 배너는 조용히 생략 (각 페이지에서 별도 안내)
        pass