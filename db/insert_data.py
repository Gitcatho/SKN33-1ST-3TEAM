import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# ── DB 설정 ──────────────────────────────────────────────
load_dotenv()

DB_USER     = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST     = os.getenv("DB_HOST")
DB_PORT     = int(os.getenv("DB_PORT", 3306))
DB_NAME     = os.getenv("DB_NAME")

# ── CSV 경로 ─────────────────────────────────────────────
REGION_CSV          = r"C:\SKN_AI\SKN33-1ST-3TEAM\data\region_df.csv"
MANUFACTURER_CSV    = r"C:\SKN_AI\SKN33-1ST-3TEAM\data\manufacturer_df.csv"
CAR_CSV             = r"C:\SKN_AI\SKN33-1ST-3TEAM\data\car_df.csv"
SERVICE_CENTER_CSV  = r"C:\SKN_AI\SKN33-1ST-3TEAM\data\service_center_df.csv"
RECALL_CSV          = r"C:\SKN_AI\SKN33-1ST-3TEAM\data\recall_df.csv"

# ────────────────────────────────────────────────────────
def main():
    engine = create_engine(
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
        echo=False
    )

    targets = [
        ("region",         REGION_CSV,         None),
        ("manufacturer",   MANUFACTURER_CSV,   None),
        ("car",            CAR_CSV,             None),
        ("service_center", SERVICE_CENTER_CSV, None),
        ("recall",         RECALL_CSV,          {"recall_reason": ""}),
    ]

    with engine.begin() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))

    for table, path, fillna_map in targets:
        df = pd.read_csv(path)

        if fillna_map:
            for col, val in fillna_map.items():
                null_count = df[col].isna().sum()
                if null_count > 0:
                    print(f"[INFO] {table}.{col} NULL {null_count}행 → '{val}'로 처리")
                    df[col] = df[col].fillna(val)

        df.to_sql(
            name=table,
            con=engine,
            if_exists="append",
            index=False,
            chunksize=1000
        )
        print(f"[OK] {table}: {len(df)}행 insert 완료")

    with engine.begin() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))

    print("\n전체 insert 완료")

if __name__ == "__main__":
    main()
