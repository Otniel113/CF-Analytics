import panel as pn
import pandas as pd
import pathlib
import plotly.express as px
import numpy as np
import joblib

def create_rating_subtab(df=None):
    # Tab Styling for sub-subtabs
    sub_tab_stylesheet = """
    .bk-tab {
        font-size: 1.1rem !important;
        padding: 12px 24px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease;
    }
    .bk-tab.bk-active {
        color: #007bff !important;
        border-bottom: 4px solid #007bff !important;
    }
    .bk-tab:hover {
        color: #007bff !important;
    }
    """

    # Intro Description
    intro_desc = pn.pane.HTML("""
        <div style="padding: 10px 0; color: #2c3e50; font-size: 1.15rem; margin-bottom: 20px;">
            <p style="margin: 0;">
                Selamat datang di Faktor Berpengaruh. Analisis di sini memiliki 2 tahap, yang pertama mencari tahu faktor yang berpengaruh dan yang kedua adalah melakukan prediksi.
                Variabel dependen atau Y atau target yang digunakan adalah Rating (GA, PG, M) dan Tipe Booth Sirkel.
            </p>
        </div>
    """, sizing_mode='stretch_width')

    # 1. Rating Age Content
    # Load feature importance data
    current_dir = pathlib.Path(__file__).parent.parent.parent
    data_path = current_dir / "data" / "df_importance_rating.pkl"
    try:
        # Check if file exists first to avoid unexpected errors
        if not data_path.exists():
            return pn.pane.Markdown(f"File not found: {data_path}")
        df_importance = joblib.load(data_path)
    except Exception as e:
        return pn.pane.Markdown(f"Error loading rating importance data: {e}")

    # Description for Rating Age
    rating_desc = pn.pane.HTML("""
        <div style="padding: 10px 0; color: #2c3e50; font-size: 1.15rem; margin-bottom: 20px;">
            <p style="margin: 0;">Mencari faktor-faktor apa saja yang mempengaruhi penentuan rating umur (GA, PG, M) pada CF.</p>
        </div>
    """, sizing_mode='stretch_width')

    # Prepare Plotly plot
    df_sorted = df_importance.sort_values(by='Importance', ascending=True)
    
    fig = px.bar(
        df_sorted,
        x='Importance',
        y='Feature',
        orientation='h',
        title="Faktor yang Mempengaruhi Rating Age (GA, PG, M)",
        template='ggplot2'
    )

    fig.update_traces(
        marker_color='#3b82f6',
        texttemplate='%{x:.3f}', 
        textposition='outside',
        cliponaxis=False
    )

    fig.update_layout(
        margin=dict(t=50, b=0, l=0, r=80),
        title_x=0.5,
        xaxis_title="Importance Score",
        yaxis_title="Feature",
        height=500,
        yaxis={'categoryorder':'total ascending'}
    )
    
    plot_pane = pn.pane.Plotly(fig, sizing_mode="stretch_width", height=500)

    # Feature Inspection (Stacked Bar Plots)
    # Highest importance first for dropdown
    feature_options = df_sorted.sort_values(by='Importance', ascending=False)['Feature'].tolist()
    feature_selector = pn.widgets.Select(name='🔍 Pilih Fitur untuk Diinspeksi', options=feature_options, sizing_mode='stretch_width')

    @pn.depends(feature_selector.param.value)
    def render_stacked_bars(selected_feature):
        if df is None or selected_feature not in df.columns:
            return pn.pane.Markdown(f"*Data kolom '{selected_feature}' tidak ditemukan di dataset utama.*", styles={'color': 'red'})

        df_valid = df.dropna(subset=['rating', selected_feature]).copy()
        
        # Ensure values are represented as '0' and '1'
        df_valid['Feature_Value'] = df_valid[selected_feature].astype(int).astype(str)

        # Plot 1: Y=Rating, Stack=Feature_Value
        counts1 = df_valid.groupby(['rating', 'Feature_Value']).size().reset_index(name='Count')
        fig1 = px.bar(
            counts1,
            y='rating',
            x='Count',
            color='Feature_Value',
            orientation='h',
            title=f"Distribusi Fitur '{selected_feature}' per Rating",
            color_discrete_map={'1': '#3b82f6', '0': '#94a3b8'}, # 1 blue, 0 gray
            template='ggplot2',
            barmode='stack',
            category_orders={'rating': ['GA', 'PG', 'M'], 'Feature_Value': ['0', '1']}
        )
        fig1.update_layout(margin=dict(t=50, b=20, l=10, r=10), title_x=0.5)

        # Plot 2: Y=Feature_Value, Stack=Rating
        counts2 = df_valid.groupby(['Feature_Value', 'rating']).size().reset_index(name='Count')
        fig2 = px.bar(
            counts2,
            y='Feature_Value',
            x='Count',
            color='rating',
            orientation='h',
            title=f"Komposisi Rating pada '{selected_feature}'",
            color_discrete_map={'GA': '#2ecc71', 'PG': '#f1c40f', 'M': '#e74c3c'}, # Green, Yellow, Red
            template='ggplot2',
            barmode='stack',
            category_orders={'Feature_Value': ['0', '1'], 'rating': ['GA', 'PG', 'M']}
        )
        fig2.update_layout(margin=dict(t=50, b=20, l=10, r=10), title_x=0.5)

        return pn.Row(
            pn.pane.Plotly(fig1, sizing_mode="stretch_both"),
            pn.pane.Plotly(fig2, sizing_mode="stretch_both"),
            sizing_mode="stretch_width",
            min_height=350
        )

    # Keterangan
    keterangan = pn.pane.HTML("""
        <div style="background-color: #f8f9fa; border-left: 5px solid #007bff; padding: 15px; border-radius: 4px; margin: 15px 0;">
            <p style="margin: 0; color: #495057;">
                <strong>Keterangan:</strong> Faktor pengaruh didapatkan dengan menggunakan Feature Importance dari Random Forest. 
                Semakin tinggi nilainya, maka semakin penting pengaruhnya.
            </p>
        </div>
    """, sizing_mode='stretch_width')

    rating_age_content = pn.Column(
        rating_desc, 
        plot_pane, 
        keterangan,
        pn.layout.Divider(),
        pn.pane.HTML("<h2 style='color: #2c3e50; margin-bottom: 10px;'>Inspeksi Detail Fitur</h2>"),
        feature_selector,
        render_stacked_bars,
        sizing_mode="stretch_width"
    )

    # 2. Tipe Booth Content (Coming Soon)
    tipe_booth_content = pn.pane.Markdown("### 🚀 Coming Soon\nTipe Booth analysis will be available here soon.")

    # Build the sub-sub-tabs
    sub_sub_tabs = pn.Tabs(
        ("Rating Age", rating_age_content),
        ("Tipe Booth", tipe_booth_content),
        stylesheets=[sub_tab_stylesheet],
        margin=(10, 0)
    )

    return pn.Column(
        intro_desc,
        sub_sub_tabs,
        sizing_mode="stretch_width"
    )
