# CF Analytics App

Bagian ini berisi aplikasi web utama untuk melakukan analisis data Comifuro secara interaktif.

## Tech Stack
- **Python**: Versi 3.10 atau yang lebih baru.
- **Panel**: Framework untuk membuat dashboard interaktif dan aplikasi data.
- **Pandas**: Digunakan untuk manipulasi dan pemrosesan data (tabel master).
- **Tabulator**: Extension Panel untuk tampilan tabel yang lebih canggih (sorting, filtering).
- **Plotly**: Library visualisasi data interaktif untuk EDA dan Trend Analysis.
- **Joblib/Pickle**: Digunakan untuk memuat data pre-processed dan pipeline machine learning (`.pkl`).
- **Scikit Learn dan Scipy**: Model statistik dan machine learning.
- **Gemini API dan Google GenAI SDK**: Model untuk Chatbot.

## Struktur Folder & File
- `assets/`: Folder berisi aset statis seperti CSS dan gambar.
- `chatbot/`: Folder berisi chatbot dan model.
- `data/`: Folder yang berisi data yang sudah diproses.
- `pipelines/`: Folder berisi model machine learning yang sudah dilatih.
- `tabs/`: Folder berisi modul-modul utama untuk setiap tab aplikasi.
- `tabs/subtabs/`: Folder berisi komponen modular/sub-tab.
- `templates/`: Struktur HTML utama menggukanakn format Jinja.
- `app.py`: File utama aplikasi dashboard.
- `.env.example`: Template environment variables.
- `requirements.txt`: Daftar dependensi Python yang dibutuhkan.

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

3. **Set Up Environment Variables:**
   Salin file `.env.example` menjadi `.env`. Buka file `.env` dan update nilainya:
   ```env
   GEMINI_API_KEY=your_actual_key_here
   GEMINI_MODEL_ID=gemini-3.1-flash-lite
   ```

4. **Menjalankan Aplikasi:**
   Terminal dalam folder `cf-analytics`:
   ```powershell
   python app.py
   ```
