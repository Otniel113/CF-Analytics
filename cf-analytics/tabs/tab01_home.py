import panel as pn

def create_tab():
    home_html = """
    <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #2c3e50; padding: 10px; font-size: 1.15rem;">
        <h1 style="color: #007bff; border-bottom: 3px solid #007bff; padding-bottom: 15px; margin-top: 0; font-size: 2.5rem;">CF (Comifuro) Analytics</h1>
        <p style="font-size: 1.3rem; margin-bottom: 25px;">
            <strong>CF (Comifuro) Analytics</strong> adalah aplikasi berbasis web yang menyajikan data lengkap, visualisasi data, dan juga analisis data tentang informasi booth-booth yang ada di acara Comifuro (sekitar 1000 lebih). Comifuro sendiri adalah salah satu acara ACG (Anime, Comic, Game) terbesar di Indonesia. Data ini didapatkan dari website Catalog Comifuro. CF Analytics ini bisa menjadi landasan berbasis data untuk mengetahui tentang kebudayaan hobi ACG ini di Indonesia.
        </p>

        <div style="background-color: #f8f9fa; border-left: 6px solid #007bff; padding: 20px; margin-bottom: 35px; border-radius: 0 12px 12px 0;">
            <h3 style="margin-top: 0; color: #0056b3; font-size: 1.8rem;">Hal yang membuat unik adalah:</h3>
            <ol style="margin-bottom: 0; font-size: 1.2rem;">
                <li style="margin-bottom: 8px;"><strong>Menggunakan fitur filter pencarian</strong> yang lebih lengkap dan berbeda dari website resmi CF.</li>
                <li style="margin-bottom: 8px;"><strong>Memiliki olah data yang komprehensif</strong> (lengkap) untuk topik hobi ini.</li>
                <li style="margin-bottom: 8px;"><strong>Memiliki data CF di masa lalu</strong>.</li>
                <li><strong>Melakukan pengelompokan</strong> ke beberapa fandom besar yang didapatkan dari hasil observasi.</li>
            </ol>
        </div>

        <h3 style="color: #27ae60; border-left: 6px solid #27ae60; padding-left: 20px; margin-bottom: 20px; font-size: 1.8rem;">Pengelompokan Fandom:</h3>
        <ul style="list-style-type: none; padding-left: 0; margin-bottom: 35px; font-size: 1.2rem;">
            <li style="margin-bottom: 15px;"><strong>Hoyoverse</strong> = Meliputi seluruh game buatan Hoyoverse seperti Honkai Impact, Genshin Impact, Honkai Star Rail, Zenless Zone Zero, dsb.</li>
            <li style="margin-bottom: 15px;"><strong>Vtuber</strong> = Virtual Youtuber, meliputi nama-nama besar seperti Hololive, Nijisanji, atau siapapun yang menggunakan kata "Vtuber".</li>
            <li style="margin-bottom: 15px;"><strong>Other Gacha</strong> = Penggemar game gacha lain di luar Hoyoverse. Ada beberapa judul yang dipertimbangkan, seperti Wuthering Waves, Blue Archive, Love and Deepspace, dsb.</li>
            <li style="margin-bottom: 15px;"><strong>V-Synth</strong> = Voice Synthesizer. Meliputi Vocaloid, Hatsune Miku, dsb. Project Sekai juga dimasukan ke sini.</li>
            <li style="margin-bottom: 15px;"><strong>Original</strong> = Bukan memakai judul orang lain, melainkan memiliki karya, produk, ataupun karakter buatan sendiri.</li>
            <li style="margin-bottom: 15px;"><strong>Other (niche)</strong> = Kategori yang tidak masuk ke dalam lima sebelumnya. Biasanya fandom judul anime tertentu masuk ke kategori ini.</li>
        </ul>

        <h3 style="color: #e67e22; border-left: 6px solid #e67e22; padding-left: 20px; margin-bottom: 20px; font-size: 1.8rem;">Fitur di CF Analytics:</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px;">
            <div style="padding: 20px; border: 1px solid #ddd; border-radius: 10px; background: #fff; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <strong style="font-size: 1.3rem; color: #d35400;">Master Data</strong><br><span style="font-size: 1.15rem;">Basis data seluruh booth di Comifuro. Bisa melakukan pencarian, filter, dan pengurutan.</span>
            </div>
            <div style="padding: 20px; border: 1px solid #ddd; border-radius: 10px; background: #fff; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <strong style="font-size: 1.3rem; color: #d35400;">Exploratory Data Analysis</strong><br><span style="font-size: 1.15rem;">Visualisasi data untuk statistik deskriptif. Untuk lebih mengetahui persebaran data CF.</span>
            </div>
            <div style="padding: 20px; border: 1px solid #ddd; border-radius: 10px; background: #fff; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <strong style="font-size: 1.3rem; color: #d35400;">Advanced Analysis</strong><br><span style="font-size: 1.15rem;">Analisis data lebih lanjut (tingkat tinggi). Menggunakan pendekatan data science seperti machine learning.</span>
            </div>
            <div style="padding: 20px; border: 1px solid #ddd; border-radius: 10px; background: #fff; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <strong style="font-size: 1.3rem; color: #d35400;">Trend Analysis</strong><br><span style="font-size: 1.15rem;">Menganalisis trending Comifuro dengan membandingkan pada acara Comifuro sebelumnya.</span>
            </div>
            <div style="padding: 20px; border: 1px solid #ddd; border-radius: 10px; background: #fff; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <strong style="font-size: 1.3rem; color: #d35400;">Chatbot</strong><br><span style="font-size: 1.15rem;">Bot AI LLM (Kofu-chan) yang bisa ditanya untuk mengetahui informasi lebih detail dan mendalam tentang katalog CF22.</span>
            </div>
        </div>
    </div>
    """
    
    return pn.Column(
        pn.pane.HTML(home_html),
        styles={'padding': '40px', 'background': '#ffffff', 'border-radius': '20px', 'border': '1px solid #e0e0e0', 'box-shadow': '0 4px 20px rgba(0,0,0,0.08)'},
        sizing_mode="stretch_width"
    )
