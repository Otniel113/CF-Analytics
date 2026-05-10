# CF-Analytics

Dashboard analitik lengkap untuk Comifuro (CF) mulai dari tabel master, visualisasi data, implementasi machine learning data science, sampai chatbot LLM.

## Deskripsi

**CF (Comifuro) Analytics** adalah aplikasi berbasis web yang menyajikan data lengkap, visualisasi data, dan juga analisis data tentang informasi booth-booth yang ada di acara Comifuro (sekitar 1000 lebih). Comifuro sendiri adalah salah satu acara ACG (Anime, Comic, Game) terbesar di Indonesia. Data ini didapatkan dari website Catalog Comifuro. CF Analytics ini bisa menjadi landasan berbasis data untuk mengetahui tentang kebudayaan hobi ACG ini di Indonesia.

### Hal yang membuat unik adalah:
1. **Menggunakan fitur filter pencarian** yang lebih lengkap dan berbeda dari website resmi CF.
2. **Memiliki olah data yang komprehensif** (lengkap) untuk topik hobi ini.
3. **Memiliki data CF di masa lalu**.
4. **Melakukan pengelompokan** ke beberapa fandom besar yang didapatkan dari hasil observasi.

### Pengelompokan Fandom:
- **Hoyoverse** = Meliputi seluruh game buatan Hoyoverse seperti Honkai Impact, Genshin Impact, Honkai Star Rail, Zenless Zone Zero, dsb.
- **Vtuber** = Virtual Youtuber, meliputi nama-nama besar seperti Hololive, Nijisanji, atau siapapun yang menggunakan kata "Vtuber".
- **Other Gacha** = Penggemar game gacha lain di luar Hoyoverse. Ada beberapa judul yang dipertimbangkan, seperti Wuthering Waves, Blue Archive, Love and Deepspace, dsb.
- **V-Synth** = Voice Synthesizer. Meliputi Vocaloid, Hatsune Miku, dsb. Project Sekai juga dimasukan ke sini.
- **Original** = Bukan memakai judul orang lain, melainkan memiliki karya, produk, ataupun karakter buatan sendiri.
- **Other (niche)** = Kategori yang tidak masuk ke dalam lima sebelumnya. Biasanya fandom judul anime tertentu masuk ke kategori ini.

## Struktur Project

Proyek ini terbagi menjadi dua bagian utama:

- **[notebooks/](notebooks/)**: Berisi file-file untuk analisis awal (*early analytics*), pembuatan model machine learning, eksplorasi data, dan eksperimen lainnya menggunakan Jupyter Notebook / Google Collab yang diubah menjadi script Python (.py).
- **[cf-analytics/](cf-analytics/)**: Berisi aplikasi dashboard utama yang siap digunakan.

## Fitur

- [x] **Home**: Halaman utama yang memberikan ringkasan proyek dan navigasi cepat.
- [x] **Master Data**: Basis data seluruh booth di Comifuro. Bisa melakukan pencarian, filter, dan pengurutan.
- [x] **Exploratory Data Analysis**: Visualisasi data untuk statistik deskriptif. Untuk lebih mengetahui persebaran data CF.
- [x] **Advanced Analysis**: Analisis data lebih lanjut (tingkat tinggi). Menggunakan pendekatan data science seperti machine learning.
- [x] **Trend Analysis**: Menganalisis trending Comifuro dengan membandingkan pada acara Comifuro sebelumnya.
- [ ] **LLM Chatbot**: Bot AI LLM yang bisa ditanya untuk mengetahui informasi lebih detail dan mendalam.
