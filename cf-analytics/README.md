# CF Analytics App

Bagian ini berisi aplikasi web utama untuk melakukan analisis data Comifuro secara interaktif.

## Tech Stack
- **Python**: Bahasa pemrograman utama.
- **Panel**: Framework untuk membuat dashboard interaktif dan aplikasi data.
- **Pandas**: Digunakan untuk manipulasi dan pemrosesan data (tabel master).
- **Tabulator**: Extension Panel untuk tampilan tabel yang lebih canggih (sorting, filtering).
- **Joblib/Pickle**: Digunakan untuk memuat data pre-processed (`.pkl`).

## Struktur Folder & File
- `app.py`: File utama aplikasi dashboard.
- `requirements.txt`: Daftar dependensi Python yang dibutuhkan.
- `data/`: Folder yang berisi data yang sudah diproses (misalnya `df_cf.pkl`).
- `README.md`: File dokumentasi teknis ini.

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
   panel serve app.py --show
   ```

## Fitur Utama
- **Pencarian Cepat**: Memungkinkan pengguna mencari circle berdasarkan nama, kode booth, atau fandom secara real-time.
- **Filtering Dinamis**: Menyediakan filter mendalam berdasarkan jenis circle, rating (mature/general), hari operasional, hingga kategori produk spesifik yang dijual.
- **Table Interaktif**: Menampilkan data master dalam format tabel yang mendukung pengurutan (*sorting*) dan penyaringan kolom untuk kemudahan analisis manual.
