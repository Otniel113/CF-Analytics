# CF Analytics App

Bagian ini berisi aplikasi web utama untuk melakukan analisis data Comifuro secara interaktif.

## Tech Stack
- **Python**: Bahasa pemrograman utama.
- **Panel**: Framework untuk membuat dashboard interaktif dan aplikasi data.
- **Pandas**: Digunakan untuk manipulasi dan pemrosesan data (tabel master).
- **Tabulator**: Extension Panel untuk tampilan tabel yang lebih canggih (sorting, filtering).
- **Plotly**: Library visualisasi data interaktif untuk EDA dan Trend Analysis.
- **Joblib/Pickle**: Digunakan untuk memuat data pre-processed (`.pkl`).

## Struktur Folder & File
- `app.py`: File utama aplikasi dashboard.
- `tabs/`: Folder berisi modul-modul untuk setiap tab aplikasi.
- `requirements.txt`: Daftar dependensi Python yang dibutuhkan.
- `data/`: Folder yang berisi data yang sudah diproses (misalnya `df_cf.pkl`).
- `assets/`: Folder berisi aset statis seperti CSS.
- `templates/`: Folder berisi template Jinja2 untuk layout web.

## Instalasi & Cara Menjalankan

1. **Persiapan Virtual Environment (Opsional tapi disarankan):**
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

2. **Instalasi Dependensi:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Menjalankan Aplikasi:**
   Terminal dalam folder `cf-analytics`:
   ```powershell
   python app.py
   ```

## Fitur Utama
- **Master Data**: Tabel interaktif untuk mencari, memfilter, dan melihat seluruh data circle Comifuro secara mendetail.
- **Exploratory Data Analysis**: Visualisasi data interaktif (Pie & Bar Charts) menggunakan Plotly untuk melihat persebaran kategori, rating, link sosial media, dan produk.
- **Trend Analysis**: Memantau perkembangan fandom dan popularitas kategori tertentu dari waktu ke waktu (antarsesi Comifuro) dengan line chart interaktif.
- **Advanced Analysis**: (Dalam Pengembangan) Analisis lebih mendalam menggunakan pendekatan data science / machine learning.
- **LLM Chatbot**: (Dalam Pengembangan) Asisten pintar berbasis AI untuk tanya jawab seputar data Comifuro.
