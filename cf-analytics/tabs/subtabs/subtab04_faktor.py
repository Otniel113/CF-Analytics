import panel as pn
import pathlib

# Import modularized detail content
from .faktor_detail.faktor_pengaruh_rating import get_rating_content
from .faktor_detail.faktor_pengaruh_type import get_type_content

def create_rating_subtab(df=None):
    # Tab Styling for sub-subtabs (Green to differentiate from main tabs)
    sub_tab_stylesheet = """
    .bk-tab {
        font-size: 1.1rem !important;
        padding: 12px 24px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease;
    }
    .bk-tab.bk-active {
        color: #10b981 !important;
        border-bottom: 4px solid #10b981 !important;
    }
    .bk-tab:hover {
        color: #10b981 !important;
    }
    """

    # Intro Description
    intro_desc = pn.pane.HTML("""
        <div style="padding: 10px 0; color: #2c3e50; font-size: 1.15rem; margin-bottom: 20px;">
            <p style="margin: 0;">
                Selamat datang di Faktor Berpengaruh. Analisis di sini memiliki 2 tahap, yang pertama mencari tahu faktor yang berpengaruh dan yang kedua adalah melakukan prediksi.
                Variabel dependen atau Y atau target yang digunakan adalah Rating (GA, PG, M) dan Tipe Booth Sirkel (1 Space, 2 Spaces, 4 Spaces, Booth A, Booth B). 
                Variabel independen atau X yang digunakan adalah apa saja yang dijual dan juga merupakan fandom apa saja.
            </p>
        </div>
    """, sizing_mode='stretch_width')

    current_dir = pathlib.Path(__file__).parent.parent.parent

    # Create sub-subtabs using modular components
    sub_sub_tabs = pn.Tabs(
        ("Rating Age", get_rating_content(df, current_dir)),
        ("Tipe Booth", get_type_content(df, current_dir)),
        stylesheets=[sub_tab_stylesheet],
        margin=(10, 0)
    )

    return pn.Column(intro_desc, sub_sub_tabs, sizing_mode="stretch_width")
