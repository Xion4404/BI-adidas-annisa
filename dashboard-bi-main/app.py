import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(
    page_title="Adidas Executive Dashboard",
    page_icon="👟",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>
    /* Background Utama: Gelap Elegan */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    /* Sidebar: Sedikit lebih terang dari background */
    section[data-testid="stSidebar"] {
        background-color: #262730;
    }
    
    /* Header Style */
    .header-container {
        background: linear-gradient(90deg, #262730 0%, #0E1117 100%);
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #00D4FF; /* Aksen Biru Muda */
        margin-bottom: 20px;
    }
    .header-title {
        font-size: 24px;
        font-weight: bold;
        color: white;
        margin: 0;
    }
    .header-subtitle {
        font-size: 14px;
        color: #A0A0A0;
        margin-top: 5px;
    }
    
    /* KPI Cards (Lonjong) - Sekarang punya warna background jelas */
    div[data-testid="stMetric"] {
        background-color: #1F2229; /* Card Gelap */
        border: 1px solid #30333F;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    /* Warna Label & Angka di KPI */
    div[data-testid="stMetricLabel"] { color: #A0A0A0 !important; font-size: 14px; }
    div[data-testid="stMetricValue"] { color: #00D4FF !important; font-size: 26px; font-weight: bold; }
    
    /* Tabs yang lebih terlihat */
    .stTabs [data-baseweb="tab"] { color: #FAFAFA; }
    .stTabs [aria-selected="true"] { color: #00D4FF !important; border-bottom-color: #00D4FF !important; }
</style>
""", unsafe_allow_html=True)
@st.cache_data
def load_data():
    df = None
    possible_paths = [
        'data/Adidas US Sales Datasets.csv',                 
        'dashboard-bi-main/data/Adidas US Sales Datasets.csv', 
        'Adidas US Sales Datasets.csv'                        
    ]
    for path in possible_paths:
        try:
            df = pd.read_csv(path, header=4)
            break
        except FileNotFoundError:
            continue
            
    if df is None:
        st.error("⚠️ FATAL ERROR: File 'Adidas US Sales Datasets.csv' tidak ditemukan di folder manapun!")
        st.stop()

    try:
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

        for col in ['Total Sales', 'Operating Profit', 'Price per Unit']:
            if col in df.columns:
                df[col] = df[col].apply(clean_currency)
            
        if 'Units Sold' in df.columns:
            df['Units Sold'] = df['Units Sold'].astype(str).str.replace(',', '').apply(lambda x: float(x) if x.replace('.','',1).isdigit() else 0.0)
        
        if 'Operating Margin' in df.columns:
            df['Operating Margin'] = df['Operating Margin'].apply(clean_percent)
    
            if df['Operating Margin'].mean() < 1.0: 
                df['Margin %'] = df['Operating Margin'] * 100
            else: 
                df['Margin %'] = df['Operating Margin']

        if 'Invoice Date' in df.columns:
            df['Invoice Date'] = pd.to_datetime(df['Invoice Date'], errors='coerce')
            df['Year'] = df['Invoice Date'].dt.year
            df['Month'] = df['Invoice Date'].dt.strftime('%Y-%m')
        
        if 'Product' in df.columns:
            df['Gender'] = df['Product'].apply(lambda x: "Men's" if "Men's" in str(x) else ("Women's" if "Women's" in str(x) else "Unisex"))
            df['Category'] = df['Product'].apply(lambda x: "Footwear" if "Footwear" in str(x) else ("Apparel" if "Apparel" in str(x) else "Gear"))
        
        return df
    except Exception as e:
        st.error(f"⚠️ Error saat membersihkan data: {e}")
        return None

df = load_data()

st.markdown("""
<div class="header-container">
    <h1 class="header-title">👟 ADIDAS SALES EXECUTIVE</h1>
    <p class="header-subtitle">Real-time Performance Monitoring System</p>
</div>
""", unsafe_allow_html=True)

if df is not None:

    with st.sidebar:
        st.header("🎛️ Filter Panel")
        
    
        valid_years = sorted([y for y in df['Year'].unique() if pd.notna(y)])
        selected_year = st.selectbox("📅 Tahun", ["All"] + [str(int(y)) for y in valid_years])

        regions = sorted([r for r in df['Region'].unique() if pd.notna(r)])
        selected_region = st.selectbox("🌍 Wilayah", ["All"] + regions)
        
        st.divider()
        
 
        page = st.radio("📂 Pindah Halaman", [
            "Overview",
            "Produk", 
            "Retailer",
            "Margin"
        ])


    df_filtered = df.copy()
    if selected_year != "All":
        df_filtered = df_filtered[df_filtered['Year'] == int(selected_year)]
    if selected_region != "All":
        df_filtered = df_filtered[df_filtered['Region'] == selected_region]

    if page == "Overview":

        try:
            k1, k2, k3, k4 = st.columns(4)
            k1.metric("Revenue", f"${df_filtered['Total Sales'].sum():,.0f}")
            k2.metric("Profit", f"${df_filtered['Operating Profit'].sum():,.0f}")
            k3.metric("Volume (Qty)", f"{df_filtered['Units Sold'].sum():,.0f}")
            k4.metric("Avg Margin", f"{df_filtered['Margin %'].mean():.1f}%")
        except Exception as e: st.warning(f"Gagal memuat KPI: {e}")
        
        st.markdown("---")
        
     
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader("Tren Penjualan Bulanan")
            try:
                trend = df_filtered.groupby(['Year', 'Month'])['Total Sales'].sum().reset_index()
                fig = px.bar(trend, x='Month', y='Total Sales', color='Year', barmode='group',
                             template='plotly_dark', color_discrete_sequence=px.colors.qualitative.Pastel)
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e: st.error(f"Grafik Tren Error: {e}")
            
        with col2:
            st.subheader("Sebaran Wilayah")
            try:
                reg = df_filtered.groupby('Region')['Total Sales'].sum().reset_index()
                fig = px.pie(reg, values='Total Sales', names='Region', hole=0.5,
                             template='plotly_dark', color_discrete_sequence=px.colors.sequential.Teal)
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e: st.error(f"Grafik Wilayah Error: {e}")

    elif page == "Produk":
        st.subheader("📦 Analisis Produk")
        
        try:
            prod_df = df_filtered.groupby(['Product', 'Category', 'Gender']).agg({
                'Total Sales': 'sum', 'Operating Profit': 'sum', 'Units Sold': 'sum', 'Margin %': 'mean'
            }).reset_index()
            
            tab1, tab2 = st.tabs(["🏆 Top Sales", "📊 Kategori"])
            
            with tab1:
                col_a, col_b = st.columns(2)
                with col_a:
                    top10 = prod_df.sort_values('Total Sales', ascending=False).head(10)
                    fig = px.bar(top10, y='Product', x='Total Sales', orientation='h', 
                                 title='Top 10 Produk Terlaris', template='plotly_dark',
                                 color='Total Sales', color_continuous_scale='Tealgrn')
                    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', yaxis={'categoryorder':'total ascending'})
                    st.plotly_chart(fig, use_container_width=True)
                with col_b:
                    fig = px.scatter(prod_df, x='Total Sales', y='Operating Profit', size='Units Sold',
                                     title='Sales vs Profit (Bubble)', template='plotly_dark',
                                     color='Category', size_max=40)
                    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
            
                fig = px.sunburst(prod_df, path=['Category', 'Gender'], values='Total Sales',
                                  title='Deep Dive: Kategori > Gender', template='plotly_dark')
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
                
        except Exception as e: st.error(f"Modul Produk Error: {e}")

    elif page == "Retailer":
        st.subheader("👥 Mitra Ritel")
        try:
            ret = df_filtered.groupby('Retailer')[['Total Sales', 'Operating Profit']].sum().reset_index()
            fig = px.bar(ret.sort_values('Total Sales'), x='Total Sales', y='Retailer', orientation='h',
                         text_auto='.2s', title='Pendapatan per Retailer', template='plotly_dark',
                         color='Operating Profit', color_continuous_scale='Purples')
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("#### Detail Data")
            st.dataframe(ret.sort_values('Total Sales', ascending=False), use_container_width=True)
        except Exception as e: st.error(f"Modul Retailer Error: {e}")


    elif page == "Margin":
        st.subheader("💰 Analisis Profitabilitas")
        try:
            c1, c2 = st.columns(2)
            with c1:
                fig = px.histogram(df_filtered, x='Margin %', nbins=20, title='Distribusi Margin',
                                   template='plotly_dark', color_discrete_sequence=['#00D4FF'])
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
            with c2:
                met = df_filtered.groupby('Sales Method')['Margin %'].mean().reset_index()
                fig = px.bar(met, x='Sales Method', y='Margin %', title='Rata-rata Margin per Metode',
                             template='plotly_dark', color='Sales Method')
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
        except Exception as e: st.error(f"Modul Margin Error: {e}")

else:
    st.info("Sedang memuat data... (Jika lama, pastikan file CSV ada di folder 'data')")
