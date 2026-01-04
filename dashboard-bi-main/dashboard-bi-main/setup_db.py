import pandas as pd
import sqlite3
import os

# Nama file
csv_file = 'data/Adidas US Sales Datasets.csv' # Sesuaikan kalau file ada di folder 'data'
db_file = 'adidas_dw.db'

# Cek apakah CSV ada?
if not os.path.exists(csv_file):
    # Coba cari di root kalau ga ada di folder data
    csv_file = 'Adidas US Sales Datasets.csv'

if os.path.exists(csv_file):
    print(f"📂 Membaca file: {csv_file}...")
    
    # 1. EXTRACT (Baca CSV)
    df = pd.read_csv(csv_file, header=4)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # 2. TRANSFORM (Bersihkan Nama Kolom biar ramah SQL)
    # SQL gasuka spasi, jadi 'Total Sales' kita ubah jadi 'Total_Sales'
    df.columns = [c.strip().replace(' ', '_').replace('.', '').replace('%', 'Pct') for c in df.columns]
    
    print("🔄 Melakukan transformasi data...")

    # 3. LOAD (Masukin ke Database)
    conn = sqlite3.connect(db_file)
    df.to_sql('fact_sales', conn, if_exists='replace', index=False)
    conn.close()
    
    print(f"✅ SUKSES! Data Warehouse siap: {db_file}")
    print(f"📊 Total Baris Data: {len(df)}")
else:
    print("❌ Error: File CSV tidak ditemukan! Pastikan posisinya benar.")