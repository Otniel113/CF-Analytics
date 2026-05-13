import panel as pn
import pandas as pd
import pathlib
import plotly.express as px
import joblib

def get_rating_content(df=None, current_dir=None):
    if current_dir is None:
        current_dir = pathlib.Path(__file__).parent.parent.parent.parent
        
    # Load feature importance data
    data_path = current_dir / "data" / "df_importance_rating.pkl"
    try:
        if not data_path.exists():
            return pn.pane.Markdown(f"File not found: {data_path}")
        df_importance = joblib.load(data_path)
        if isinstance(df_importance, dict) and 'mean_importance' in df_importance:
            df_importance = df_importance['mean_importance']
        elif isinstance(df_importance, dict):
            df_importance = pd.DataFrame(list(df_importance.items()), columns=['Feature', 'Importance'])
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
        margin=dict(t=60, b=0, l=0, r=80),
        title_x=0.5,
        xaxis_title="Importance Score",
        yaxis_title="Feature",
        height=500,
        yaxis={'categoryorder':'total ascending'}
    )

    plot_pane = pn.pane.Plotly(fig, sizing_mode="stretch_width", height=500)

    # Feature Inspection (Stacked Bar Plots)
    feature_options = df_sorted.sort_values(by='Importance', ascending=False)['Feature'].tolist()
    feature_selector = pn.widgets.Select(name='🔍 Pilih Variabel untuk Diinspeksi', options=feature_options, sizing_mode='stretch_width')

    @pn.depends(feature_selector.param.value)
    def render_stacked_bars(selected_feature):
        if df is None or selected_feature not in df.columns:
            return pn.pane.Markdown(f"*Data kolom '{selected_feature}' tidak ditemukan di dataset utama.*", styles={'color': 'red'})

        df_valid = df.dropna(subset=['rating', selected_feature]).copy()
        df_valid['Feature_Value'] = df_valid[selected_feature].astype(int).astype(str)

        # Plot 1: Y=Rating, Stack=Feature_Value
        counts1 = df_valid.groupby(['rating', 'Feature_Value']).size().reset_index(name='Count')
        fig1 = px.bar(
            counts1,
            y='rating',
            x='Count',
            color='Feature_Value',
            orientation='h',
            title=f"Distribusi '{selected_feature}' per Rating",
            color_discrete_map={'1': '#3b82f6', '0': '#94a3b8'}, # 1 blue, 0 gray
            template='ggplot2',
            barmode='stack',
            category_orders={'rating': ['GA', 'PG', 'M'], 'Feature_Value': ['0', '1']}
        )
        fig1.update_layout(margin=dict(t=60, b=20, l=10, r=10), title_x=0.5)

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
        fig2.update_layout(margin=dict(t=60, b=20, l=10, r=10), title_x=0.5)

        return pn.FlexBox(
            pn.pane.Plotly(fig1, sizing_mode="stretch_width", min_width=350, styles={'flex': '1 1 45%'}, height=350),
            pn.pane.Plotly(fig2, sizing_mode="stretch_width", min_width=350, styles={'flex': '1 1 45%'}, height=350),
            sizing_mode="stretch_width",
            justify_content='center'
        )

    keterangan = pn.pane.HTML("""
        <div style="background-color: #f8f9fa; border-left: 5px solid #007bff; padding: 15px; border-radius: 4px; margin: 15px 0;">
            <p style="margin: 0; color: #495057;">
                <strong>Keterangan:</strong> Faktor pengaruh didapatkan dengan menggunakan Feature Importance dari Random Forest.
                Semakin tinggi nilainya, maka semakin penting pengaruhnya. Kekurangan dari Feature Importance Random Forest adalah hanya bisa mendapatkan
                faktor yang berpengaruh saja, tanpa melihat arah pengaruhnya (positif atau negatif). Namun memiliki kelebihan bisa menangkap pola yang kompleks seperti interaksi antar variabel.
            </p>
        </div>
    """, sizing_mode='stretch_width')

    rating_age_content = pn.Column(
        rating_desc,
        plot_pane,
        keterangan,
        pn.layout.Divider(),
        pn.pane.HTML("<h2 style='color: #2c3e50; margin-bottom: 10px;'>Inspeksi Detail Faktor</h2>"),
        feature_selector,
        render_stacked_bars,
        sizing_mode="stretch_width"
    )

    # --- Model Prediction ---
    model_path = current_dir / "pipelines" / "prediksi_rating_pipeline.pkl"
    try:
        model = joblib.load(model_path)
        feature_cols = [
            'SellsCommision', 'SellsComic', 'SellsArtbook', 'SellsPhotobookGeneral',
            'SellsNovel', 'SellsGame', 'SellsMusic', 'SellsGoods', 'SellsHandmadeCrafts',
            'SellsMagazine', 'SellsPhotobookCosplay', 'Hoyoverse', 'Vtuber',
            'Other Gacha', 'V-Synth', 'Original', 'Other (Niche)'
        ]

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

        mid = len(toggle_rows) // 2
        left_toggles  = toggle_rows[:mid]
        right_toggles = toggle_rows[mid:]

        color_map = {
            'GA': {'bg': '#d4edda', 'border': '#28a745', 'text': '#155724'},
            'PG': {'bg': '#fff3cd', 'border': '#ffc107', 'text': '#856404'},
            'M':  {'bg': '#f8d7da', 'border': '#dc3545', 'text': '#721c24'},
        }

        prediction_output = pn.pane.HTML("", width=280, min_height=200)

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

            prediction_output.object = f"""
            <div style="background-color:{colors['bg']}; border:2px solid {colors['border']}; 
                        padding:20px; border-radius:12px; text-align:center;">
                <p style="margin:0; font-size:1.1rem; color:{colors['text']}; font-weight:500;">Prediksi Rating:</p>
                <h1 style="margin:10px 0; font-size:3.5rem; color:{colors['text']}; line-height:1;">{pred}</h1>
                <div style="margin-top:15px; text-align:left; border-top:1px solid {colors['border']}; padding-top:12px;">
                    {proba_rows}
                </div>
            </div>
            """

        update_prediction(*[toggles[feat].value for feat in feature_cols])

        prediction_section = pn.Column(
            pn.layout.Divider(),
            pn.pane.HTML("<h2 style='color: #2c3e50; margin-bottom: 5px;'>Prediksi Rating</h2>"),
            pn.FlexBox(
                pn.Column(*left_toggles, sizing_mode="stretch_width", min_width=250, styles={'flex': '1 1 30%'}),
                pn.Column(*right_toggles, sizing_mode="stretch_width", min_width=250, styles={'flex': '1 1 30%'}),
                pn.Column(prediction_output, min_width=280, styles={'flex': '1 1 30%'}, margin=(10, 0)),
                sizing_mode="stretch_width",
                justify_content='center'
            ),
            pn.pane.HTML("""
                <div style="background-color: #f8f9fa; border-left: 5px solid #28a745; padding: 15px; border-radius: 4px; margin-top: 15px;">
                    <p style="margin: 0; color: #495057;">
                        <strong>Keterangan:</strong> Hasil prediksi dan nilai peluang didapatkan dengan menggunakan machine learning Random Forest.
                    </p>
                </div>
            """, sizing_mode='stretch_width'),
            sizing_mode="stretch_width"
        )
        rating_age_content.append(prediction_section)
    except Exception as e:
        rating_age_content.append(pn.pane.Markdown(f"**Gagal memuat model prediksi:** {e}"))
    
    return rating_age_content
