import pandas as pd

df = pd.read_csv(r'C:\SKN_AI\SKN33-1ST-3TEAM\data\한국교통안전공단_차종별 리콜대수_20251231.csv', encoding='cp949')

# 제작자 중복 제거
manufacturer_df = df[['제작자']].drop_duplicates().reset_index(drop=True)
manufacturer_df['manufacturer_id'] = manufacturer_df.index + 1
manufacturer_df.columns = ['name', 'manufacturer_id']
manufacturer_df['country'] = manufacturer_df['name'].apply(
    lambda x: '국산' if x in ['현대자동차', '기아', '한국지엠', '르노코리아', '케이지모빌리티', '케이지모빌리티커머셜'] else '수입'
)
manufacturer_df = manufacturer_df[['manufacturer_id', 'name', 'country']]

manufacturer_df.to_csv(r'C:\SKN_AI\SKN33-1ST-3TEAM\data\manufacturer_df.csv', index=False, encoding='utf-8-sig')
print(f'총 {len(manufacturer_df)}개 제조사 저장 완료')
print(manufacturer_df.head(10))