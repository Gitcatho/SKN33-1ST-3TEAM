import pandas as pd

df = pd.read_csv(r'C:\SKN_AI\SKN33-1ST-3TEAM\data\한국교통안전공단_차종별 리콜대수_20251231.csv', encoding='cp949')
car_df = pd.read_csv(r'/data/car_df.csv', encoding='utf-8-sig')
manufacturer_df = pd.read_csv(r'/data/manufacturer_df.csv', encoding='utf-8-sig')

# car_id 매핑
recall_df = df.merge(manufacturer_df[['manufacturer_id', 'name']], left_on='제작자', right_on='name', how='left')
recall_df = recall_df.merge(car_df[['car_id', 'model_name', 'manufacturer_id']],
                             left_on=['차명', 'manufacturer_id'],
                             right_on=['model_name', 'manufacturer_id'], how='left')

recall_df = recall_df[['제작자', '차명', '생산기간(부터)', '생산기간(까지)', '리콜개시일', '리콜대수', '리콜사유', 'car_id']]
recall_df.columns = ['manufacturer', 'model_name', 'prod_start', 'prod_end', 'recall_date', 'recall_count', 'recall_reason', 'car_id']
recall_df['recall_id'] = recall_df.index + 1
recall_df['defect_id'] = None  # 나중에 분류 후 채움

recall_df = recall_df[['recall_id', 'prod_start', 'prod_end', 'recall_date', 'recall_count', 'recall_reason', 'car_id', 'defect_id']]

recall_df.to_csv(r'C:\SKN_AI\SKN33-1ST-3TEAM\data\recall_df.csv', index=False, encoding='utf-8-sig')
print(f'총 {len(recall_df)}개 리콜 저장 완료')
print(recall_df.head(10))