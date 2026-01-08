import os  # <--- Tambahkan ini di paling atas file jika belum ada

# ... (kode konfigurasi halaman biarkan sama) ...

# -----------------------------------------------------------------------------
# 2. LOAD DATA (ANTI-CRASH & PATH FIX)
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    try:
        # --- PERBAIKAN PATH DI SINI ---
        # 1. Cari folder dimana app.py berada
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 2. Gabungkan dengan folder 'data' dan nama file
        # Pastikan nama file di GitHub SAMA PERSIS (huruf besar/kecil/spasi)
        file_path = os.path.join(base_dir, 'data', 'Adidas US Sales Datasets.csv')

        # 3. Cek dulu apakah file benar-benar ada sebelum baca
        if not os.path.exists(file_path):
            st.error(f"❌ File tidak ditemukan di: {file_path}")
            st.info("💡 Tips: Pastikan folder 'data' dan file CSV sudah di-upload ke GitHub.")
            return None

        # 4. Baca CSV
        df = pd.read_csv(file_path, header=4)
        
        # --- Lanjutkan logika pembersihan data kamu ---
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        
        def clean_currency(x):
            try:
                if isinstance(x, str):
                    return float(x.replace('$', '').replace(',', '').replace(' ', '').strip())
                return float(x)
            except:
                return 0.0

        def clean_percent(x):
            try:
                if isinstance(x, str):
                    return float(x.replace('%', '').replace(' ', '').strip())
                return float(x)
            except:
                return 0.0

        # Bersihkan Kolom Uang
        for col in ['Total Sales', 'Operating Profit', 'Price per Unit']:
            if col in df.columns:
                df[col] = df[col].apply(clean_currency)
            
        # Bersihkan Units Sold
        if 'Units Sold' in df.columns:
            df['Units Sold'] = df['Units Sold'].astype(str).str.replace(',', '').apply(lambda x: float(x) if x.replace('.','',1).isdigit() else 0.0)
        
        # Bersihkan Margin
        if 'Operating Margin' in df.columns:
            df['Operating Margin'] = df['Operating Margin'].apply(clean_percent)
            # Logika koreksi margin kamu
            if df['Operating Margin'].mean() < 1.0: # Asumsi data desimal (0.5)
                 df['Margin %'] = df['Operating Margin'] * 100
            else:
                 df['Margin %'] = df['Operating Margin']

        # Format Tanggal
        if 'Invoice Date' in df.columns:
            df['Invoice Date'] = pd.to_datetime(df['Invoice Date'], errors='coerce')
            df['Year'] = df['Invoice Date'].dt.year
            df['Month'] = df['Invoice Date'].dt.strftime('%Y-%m')
        
        # Tambah Kategori
        if 'Product' in df.columns:
            df['Gender'] = df['Product'].apply(lambda x: "Men's" if "Men's" in str(x) else ("Women's" if "Women's" in str(x) else "Unisex"))
            df['Category'] = df['Product'].apply(lambda x: "Footwear" if "Footwear" in str(x) else ("Apparel" if "Apparel" in str(x) else "Gear"))
        
        return df

    except Exception as e:
        st.error(f"⚠️ Error Fatal Data: {e}")
        return None
