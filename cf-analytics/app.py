import pandas as pd
import panel as pn
import numpy as np
import joblib
import os

# Import tabs
from tabs import tab01_home, tab02_master_data, tab03_ed_analysis, tab04_advanced_analysis, tab05_trend_analysis, tab06_chatbot

# 1. Initialize Panel and Tabulator (required for advanced tables)
pn.extension('plotly', 'tabulator', sizing_mode="stretch_width")

# ==========================================
# DATA LOADING
# ==========================================
def load_data():
    file_path = os.path.join(os.path.dirname(__file__), 'data', 'df_cf.pkl')
    try:
        df = joblib.load(file_path)
    except Exception as e:
        print(f"Error loading df_cf: {e}")
        df = None
        
    ret_file_path = os.path.join(os.path.dirname(__file__), 'data', 'df_returning.pkl')
    try:
        df_returning = joblib.load(ret_file_path)
    except Exception as e:
        print(f"Error loading df_returning: {e}")
        df_returning = None
        
    return df, df_returning

df, df_returning = load_data()

# ==========================================
# BUILD THE UI LAYOUT
# ==========================================

main_tab_stylesheet = """
.bk-tabs-header {
    background-color: #f1f3f5 !important;
    padding-top: 10px !important;
    border-radius: 12px 12px 0 0 !important;
}
.bk-tab {
    font-size: 1.3rem !important;
    padding: 15px 30px !important;
    font-weight: 600 !important;
    border: none !important;
    background: transparent !important;
    color: #495057 !important;
}
.bk-tab.bk-active {
    background-color: #ffffff !important;
    color: #007bff !important;
    font-weight: 700 !important;
    border-radius: 10px 10px 0 0 !important;
}
"""

# The Main Tabs for the whole application
main_tabs = pn.Tabs(
    ('Home', tab01_home.create_tab()),
    ('Master Data', tab02_master_data.create_tab(df)),
    ('Exploratory Data Analysis', tab03_ed_analysis.create_tab(df)),
    ('Advanced Analysis', tab04_advanced_analysis.create_tab(df)),
    ('Trend Analysis', tab05_trend_analysis.create_tab(df, df_returning)),
    ('Chatbot', tab06_chatbot.create_tab(df)),
    dynamic=True, # Only renders the tab when clicked, saving performance
    stylesheets=[main_tab_stylesheet]
)

# Load Custom Jinja Template
template_path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
with open(template_path, 'r', encoding='utf-8') as f:
    template_html = f.read()

template = pn.Template(template_html)
template.add_panel('main_tabs', main_tabs)

template.servable()

if __name__ == '__main__':
    # Running this via `python app.py` will serve it on the root URL path (/)
    # We specify a fixed port to avoid random port assignment each time
    pn.serve({'/': template}, port=5006, show=True, static_dirs={'assets': './assets'}, title="CF Analytics")
