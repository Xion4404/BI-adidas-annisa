import pandas as pd
import sqlite3
import os

# Nama file CSV (Sesuaikan dengan nama file kamu di folder)
# Kita pakai try-except biar dia nyari sendiri
csv_possibilities = [
    'data/Adidas US Sales Datasets.csv',
    'Adidas US Sales Datasets.csv'
]

csv_file = None
for path in csv_possibilities:
    if os.path.exists(path):
        csv_file = path
        break

db_file = 'adidas_dw.db'

if csv_file:
    print(f"📂 Membaca file: {csv_file}...")
    
    # 1. EXTRACT
    df = pd.read_csv(csv_file, header=4)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # 2. TRANSFORM (Bersihkan spasi di nama kolom)
    df.columns = [c.strip().replace(' ', '_').replace('.', '').replace('%', 'Pct') for c in df.columns]
    
    print("🔄 Melakukan transformasi data...")

    # 3. LOAD (Simpan ke SQLite)
    conn = sqlite3.connect(db_file)
    df.to_sql('fact_sales', conn, if_exists='replace', index=False)
    conn.close()
    
    print(f"✅ SUKSES! Data Warehouse siap: {db_file}")
    print(f"📊 Total Baris Data: {len(df)}")
else:
    print("❌ Error: File CSV tidak ditemukan! Cek apakah file 'Adidas US Sales Datasets.csv' ada di folder ini?")