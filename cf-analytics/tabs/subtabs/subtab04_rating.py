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
            pn.pane.Plotly(fig1, sizing_mode="stretch_width", height=350),
            pn.pane.Plotly(fig2, sizing_mode="stretch_width", height=350),
            sizing_mode="stretch_width",
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

    # --- 3. Model Prediction ---
    model_path = current_dir / "pipelines" / "prediksi_rating_pipeline.pkl"
    try:
        model = joblib.load(model_path)

        feature_cols = [
            'SellsCommision', 'SellsComic', 'SellsArtbook', 'SellsPhotobookGeneral',
            'SellsNovel', 'SellsGame', 'SellsMusic', 'SellsGoods', 'SellsHandmadeCrafts',
            'SellsMagazine', 'SellsPhotobookCosplay', 'Hoyoverse', 'Vtuber',
            'Other Gacha', 'V-Synth', 'Original', 'Other (Niche)'
        ]

        # button_type='primary' makes ALL buttons the same blue — active state
        # is indistinguishable. Use 'default' + CSS: inactive=white, active=blue.
        toggle_btn_style = """
        .bk-btn.bk-btn-default {
            background-color: #ffffff;
            border: 1px solid #dee2e6;
            color: #495057;
            transition: background-color 0.15s ease, color 0.15s ease;
        }
        .bk-btn.bk-btn-default.bk-active {
            background-color: #007bff !important;
            border-color: #007bff !important;
            color: #ffffff !important;
            font-weight: 600;
        }
        .bk-btn.bk-btn-default:hover:not(.bk-active) {
            background-color: #e7f1ff !important;
            border-color: #007bff !important;
            color: #007bff !important;
        }
        """

        toggles = {
            feat: pn.widgets.RadioButtonGroup(
                options=['No', 'Yes'], value='No', button_type='default',
                width=110, stylesheets=[toggle_btn_style]
            )
            for feat in feature_cols
        }

        # Styled toggle rows — label left, toggle right, consistent alignment
        toggle_rows = []
        for feat in feature_cols:
            toggle_rows.append(pn.Row(
                pn.pane.HTML(
                    f"<span style='display:flex; align-items:center; height:100%; "
                    f"color:#2c3e50; font-weight:500; font-size:0.95rem;'>{feat}</span>",
                    width=180, height=36
                ),
                toggles[feat],
                align='center',
                margin=(3, 0)
            ))

        # Split into two equal halves for a 2-column grid
        mid = len(toggle_rows) // 2
        left_toggles  = toggle_rows[:mid]
        right_toggles = toggle_rows[mid:]

        # Color palette per rating — fixed height prevents collapse-overlap
        color_map = {
            'GA': {'bg': '#d4edda', 'border': '#28a745', 'text': '#155724'},
            'PG': {'bg': '#fff3cd', 'border': '#ffc107', 'text': '#856404'},
            'M':  {'bg': '#f8d7da', 'border': '#dc3545', 'text': '#721c24'},
        }

        prediction_output = pn.pane.HTML(
            "",
            width=280,
            min_height=200  # reserve space so layout never collapses to 0px
        )

        @pn.depends(*[toggles[feat].param.value for feat in feature_cols], watch=True)
        def update_prediction(*values):
            input_data = [1 if val == 'Yes' else 0 for val in values]
            df_input = pd.DataFrame([input_data], columns=feature_cols)

            pred = model.predict(df_input)[0]
            pred_proba = model.predict_proba(df_input)[0]
            classes = model.classes_

            colors = color_map.get(pred, color_map['GA'])

            proba_rows = "".join([
                f"<div style='display:flex; justify-content:space-between; "
                f"padding:5px 0; border-bottom:1px solid rgba(0,0,0,0.07);'>"
                f"<span style='font-weight:600;'>{c}</span>"
                f"<span>{p:.2%}</span></div>"
                for c, p in zip(classes, pred_proba)
            ])

            html_result = f"""
            <div style="background-color:{colors['bg']}; border-left:5px solid {colors['border']};
                        padding:15px 20px; border-radius:4px; margin:15px 0;">
                <h3 style="margin:0 0 10px 0; color:{colors['text']};">Prediksi Rating: <strong>{pred}</strong></h3>
                <p style="margin:0 0 8px 0; font-weight:600; color:{colors['text']};">Peluang:</p>
                <div style="color:{colors['text']};">{proba_rows}</div>
            </div>
            """
            prediction_output.object = html_result

        # Initial prediction on load
        update_prediction(*[toggles[feat].value for feat in feature_cols])

        prediction_section = pn.Column(
            pn.layout.Divider(),
            pn.pane.HTML("""
                <h2 style='color: #2c3e50; margin-bottom: 5px;'>Prediksi Rating</h2>
                <p style='color: #6c757d; margin-top: 0; font-size: 1rem;'>
                    Pilih konfigurasi booth untuk melihat prediksi Rating (GA, PG, M).
                    Bisa digunakan oleh pemilik booth sirkel untuk menentukan rating umur berdasarkan apa yang dijual dan juga merupakan fandom apa saja.
                </p>
            """, sizing_mode='stretch_width'),
            pn.pane.HTML("""
                <div style="background-color:#f8f9fa; border-left:5px solid #007bff;
                            padding:15px; border-radius:4px; margin-bottom:12px;">
                    <p style="margin:0; color:#495057;">
                        <strong>Keterangan:</strong> Prediksi dan peluang dihitung menggunakan model machine learning Random Forest.
                    </p>
                </div>
            """, sizing_mode='stretch_width'),
            pn.Row(
                # Left: toggle configuration — stretches to fill available space
                pn.Column(
                    pn.pane.HTML(
                        "<p style='font-weight:600; color:#2c3e50; margin:0 0 6px 0;'>⚙️ Konfigurasi Booth</p>",
                        sizing_mode='stretch_width'
                    ),
                    pn.Row(
                        pn.Column(*left_toggles,  sizing_mode="stretch_width"),
                        pn.Column(*right_toggles, sizing_mode="stretch_width"),
                        sizing_mode="stretch_width",
                    ),
                    sizing_mode="stretch_width",
                ),
                # Right: compact result box — fixed width, sits beside the toggles
                pn.Column(
                    pn.pane.HTML(
                        "<p style='font-weight:600; color:#2c3e50; margin:0 0 6px 0;'>Hasil Prediksi</p>",
                        width=280
                    ),
                    prediction_output,
                    width=280,
                    margin=(0, 0, 0, 20),
                ),
                sizing_mode="stretch_width",
                align="start",
            ),
            sizing_mode="stretch_width"
        )

        rating_age_content.append(prediction_section)

    except Exception as e:
        rating_age_content.append(pn.pane.Markdown(f"**Gagal memuat model prediksi:** {e}"))
    # ---------------------------

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
