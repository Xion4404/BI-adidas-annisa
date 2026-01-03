# Amazon SaaS Analytics Hub

Selamat datang di Amazon SaaS Analytics Hub, sebuah proyek Business Intelligence (BI) end-to-end. Proyek ini mendemonstrasikan proses lengkap mulai dari **Extract, Transform, Load (ETL)** data mentah dari file CSV, menstrukturkannya ke dalam model _star schema_ di dalam **Data Warehouse MySQL**, hingga menyajikannya dalam sebuah **dashboard analitik yang interaktif dan canggih** menggunakan Streamlit.

## 🚀 Fitur Utama

- **Dashboard Interaktif:** Antarmuka yang sepenuhnya interaktif dengan tema futuristik/holografik yang imersif.
- **Analisis Strategis:** Tampilan ringkasan eksekutif dengan KPI utama, tren penjualan, dan performa segmen secara _real-time_.
- **Wawasan Pelanggan:** Modul analisis mendalam untuk memahami kontribusi dan perilaku setiap segmen pelanggan.
- **Analisis Matriks Produk:** Analisis portofolio produk berdasarkan penjualan, kuantitas, dan yang terpenting, **profitabilitas**.
- **Kecerdasan Diskon:** Modul analisis statistik canggih untuk mengevaluasi dampak strategi diskon terhadap profit, lengkap dengan rekomendasi otomatis.
- **Filtering Dinamis:** Kemampuan untuk memfilter seluruh data berdasarkan tahun dan wilayah untuk analisis yang granular.

## 🛠️ Arsitektur & Teknologi

| Komponen                  | Teknologi yang Digunakan    |
| ------------------------- | --------------------------- |
| **Bahasa Pemrograman**    | Python 3.9+                 |
| **Proses ETL**            | Pandas                      |
| **Data Warehouse**        | MySQL                       |
| **Framework Dashboard**   | Streamlit                   |
| **Visualisasi Data**      | Plotly, Plotly Express      |
| **Analisis Statistik**    | SciPy                       |
| **Server Lokal**          | Laragon (menyediakan MySQL) |
| **Server Produksi**       | Ubuntu Server 22.04 LTS     |
| **Proxy, CDN & Keamanan** | Cloudflare                  |

## ⚙️ Instalasi & Konfigurasi Lokal

Ikuti langkah-langkah berikut untuk menjalankan proyek ini di mesin lokal Anda.

### Prasyarat

- [Git](https://git-scm.com/)
- [Python 3.9+](https://www.python.org/downloads/)
- [Laragon](https://laragon.org/download/) (atau XAMPP/MAMP/instalasi MySQL manual lainnya)

### Langkah-langkah Instalasi

**1. Clone Repository**

```bash
git clone https://github.com/paybackretr0/dashboard-bi.git
cd nama-repo
```

**2. Setup Database MySQL dengan Laragon**

- Jalankan Laragon.
- Klik tombol **"Start All"**. Ini akan menjalankan Apache dan MySQL.
- Klik tombol **"Database"**. Ini akan membuka HeidiSQL atau klien database default Anda.
- Buat database baru dengan nama `saas_sales_dw`.
- **PENTING:** Buka file `db/db_config.py` dan sesuaikan konfigurasi koneksi (`host`, `user`, `password`, `database`) agar sesuai dengan pengaturan Laragon Anda. Biasanya, `user` adalah `root` dan `password` kosong.

**3. Setup Lingkungan Python**

- Buat sebuah virtual environment:
  ```bash
  python -m venv venv
  ```
- Aktifkan virtual environment:
  - Windows: `.\venv\Scripts\activate`
  - macOS/Linux: `source venv/bin/activate`
- Install semua library yang dibutuhkan dari file `requirements.txt`:
  ```bash
  pip install -r requirements.txt
  ```

**4. Jalankan Proses ETL**

- Sebelum dashboard bisa menampilkan data, Anda harus mengisi database terlebih dahulu. Jalankan skrip ETL:
  ```bash
  python etl/etl_pipeline.py
  ```
- Tunggu hingga proses selesai. Anda akan melihat pesan bahwa data telah berhasil dimasukkan ke dalam tabel `dim_product`, `dim_customer`, `fact_sales`, dll.

**5. Jalankan Aplikasi Streamlit**

- Setelah database terisi, jalankan aplikasi dashboard:
  ```bash
  streamlit run app.py
  ```
- Buka browser Anda dan akses alamat yang ditampilkan (biasanya `http://localhost:8501`).

## 🚀 Deployment ke Server Ubuntu & Cloudflare

Berikut adalah panduan untuk mendeploy aplikasi ini ke server produksi.

### Prasyarat

- Sebuah server dengan **Ubuntu 22.04 LTS**.
- Akses SSH ke server tersebut.
- Sebuah nama domain yang dikelola melalui **Cloudflare**.

### Langkah-langkah Deployment

**1. Persiapan Server Ubuntu**

- Login ke server Anda melalui SSH.
- Update dan upgrade paket:
  ```bash
  sudo apt update && sudo apt upgrade -y
  ```
- Install Python, PIP, dan venv:
  ```bash
  sudo apt install python3-pip python3-venv -y
  ```
- Install Git:
  ```bash
  sudo apt install git -y
  ```

**2. Deploy Kode Aplikasi**

- Clone repository Anda ke direktori home atau `/var/www`:
  ```bash
  git clone https://github.com/paybackretr0/dashboard-bi.git
  cd nama-repo
  ```
- Buat dan aktifkan virtual environment seperti pada langkah lokal.
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
- **PENTING:** Pastikan file `db/db_config.py` di server telah dikonfigurasi untuk terhubung ke database produksi Anda (bisa di server yang sama atau database terkelola).

**3. Jalankan Streamlit sebagai Service (menggunakan `systemd`)**

- Ini memastikan aplikasi Anda berjalan secara otomatis saat server booting dan akan restart jika terjadi crash.

- Buat file service baru:

  ```bash
  sudo nano /etc/systemd/system/streamlit_app.service
  ```

- Salin dan tempel konfigurasi berikut ke dalam file tersebut. **Sesuaikan `User` dan path di `WorkingDirectory` & `ExecStart`**.

  ```ini
  [Unit]
  Description=Streamlit Analytics Hub App
  After=network.target

  [Service]
  User=namauserubuntu
  Group=namauserubuntu
  WorkingDirectory=/home/namauserubuntu/nama-repo
  ExecStart=/home/namauserubuntu/nama-repo/venv/bin/streamlit run app.py --server.port 8501 --server.address 0.0.0.0

  [Install]
  WantedBy=multi-user.target
  ```

- Simpan file (`Ctrl+X`, lalu `Y`, lalu `Enter`).

- Reload, enable, dan start service:

  ```bash
  sudo systemctl daemon-reload
  sudo systemctl enable streamlit_app.service
  sudo systemctl start streamlit_app.service
  ```

- Cek status service untuk memastikan tidak ada error:

  ```bash
  sudo systemctl status streamlit_app.service
  ```

**4. Konfigurasi Cloudflare**

- Login ke dashboard Cloudflare.
- Pilih domain.
- Pergi ke menu **DNS -\> Records**.
- Klik **"Add record"** dan buat record baru dengan konfigurasi berikut:
  - **Type:** `A`
  - **Name:** `dashboard` (atau subdomain lain yang diinginkan, misal: `analitik`). Ini akan membuat aplikasi dapat diakses di `dashboard.domain.com`).
  * **IPv4 address:** Alamat IP Publik dari server Ubuntu.
  * **Proxy status:** Pastikan ikon awan berwarna **Oranye (Proxied)**. Ini sangat penting.
- Pergi ke menu **SSL/TLS -\> Overview**.
- Set mode enkripsi SSL/TLS ke **Full (Strict)** untuk keamanan maksimal.

Tunggu beberapa menit untuk propagasi DNS. Sekarang, aplikasi dashboard seharusnya sudah bisa diakses secara publik melalui subdomain yang buat, dengan keamanan dan kecepatan dari Cloudflare.

## 📁 Struktur File Proyek (Contoh)

```
.
├── dashboard/
│   ├── customer_segmentation.py
│   ├── customer_table.py
│   ├── discount_analysis.py
│   ├── kpi_cards.py
│   ├── product_profitability.py
│   ├── region_summary.py
│   ├── sales_trends.py
│   └── top_products.py
├── data/
│   └── SaaS-Sales.csv
├── db/
│   └── db_config.py
├── etl/
│   └── etl_pipeline.py
├── app.py                  # File utama Streamlit
├── check_db_structure.py
├── requirements.txt        # Daftar library Python
└── README.md
```

## ✍️ Author

- **[Fajrin Putra Pratama]** - _Ketua Tim_
- **[Ziggy Yafi Hisyam]** - _Anggota 1_
- **[Khalied Nauly Maturino]** - _Anggota 2_
