import csv
import mysql.connector

# MySQL 연결

conn = mysql.connector.connect(
    host="localhost",
    user="skn_ai",
    password="1234",
    database="recallcardb"
)

cursor = conn.cursor()

csv_path = "../data/faq_data.csv"

with open(csv_path, "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)

    for row in reader:
        sql = """
        INSERT INTO faq (
            faq_id,
            question,
            answer
        )
        VALUES (%s, %s, %s)
        """

        values = (
            int(row["faq_id"]),
            row["question"],
            row["answer"]
        )

        cursor.execute(sql, values)

conn.commit()

print("FAQ 데이터 저장 완료")

cursor.close()
conn.close()