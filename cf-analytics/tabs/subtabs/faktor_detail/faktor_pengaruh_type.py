import panel as pn
import pandas as pd
import pathlib
import plotly.express as px
import joblib

def get_type_content(df=None, current_dir=None):
    if current_dir is None:
        current_dir = pathlib.Path(__file__).parent.parent.parent.parent
        
    data_path = current_dir / "data" / "df_importance_circle_type.pkl"
    try:
        if not data_path.exists():
            return pn.pane.Markdown(f"File not found: {data_path}")
        importance_data = joblib.load(data_path)
        if isinstance(importance_data, dict) and 'mean_importance' in importance_data:
            df_importance = importance_data['mean_importance']
        elif isinstance(importance_data, dict):
            df_importance = pd.DataFrame(list(importance_data.items()), columns=['Feature', 'Importance'])
        else:
            df_importance = importance_data
    except Exception as e:
        return pn.pane.Markdown(f"Error loading circle type importance data: {e}")

    type_desc = pn.pane.HTML("""
        <div style="padding: 10px 0; color: #2c3e50; font-size: 1.15rem; margin-bottom: 20px;">
            <p style="margin: 0;">Mencari faktor-faktor apa saja yang mempengaruhi penentuan tipe booth sirkel (1 Space, 2 Spaces, 4 Spaces, Booth A, Booth B) pada CF.</p>
        </div>
    """, sizing_mode='stretch_width')

    df_sorted = df_importance.sort_values(by='Importance', ascending=True)
    fig = px.bar(df_sorted, x='Importance', y='Feature', orientation='h', title="Faktor yang Mempengaruhi Tipe Booth Sirkel", template='ggplot2')
    fig.update_traces(marker_color='#f59e0b', texttemplate='%{x:.3f}', textposition='outside', cliponaxis=False)
    fig.update_layout(margin=dict(t=50, b=0, l=0, r=80), title_x=0.5, xaxis_title="Importance Score", yaxis_title="Feature", height=500, yaxis={'categoryorder':'total ascending'})
    plot_pane = pn.pane.Plotly(fig, sizing_mode="stretch_width", height=500)

    # Coefficient Table
    coef_pane = pn.Column()
    try:
        if isinstance(importance_data, dict) and 'coefficients_per_class' in importance_data:
            coef_df = importance_data['coefficients_per_class']
            
            # Manual color scaling with pastel colors to avoid matplotlib dependency
            def color_scale(val):
                # Pastel RdBu-like scale: Negative (Pastel Red) -> 0 (White) -> Positive (Pastel Blue)
                # Clamp value between -2 and 2 for scaling
                v = max(-2, min(2, val))
                if v < 0:
                    # Pastel Red for negative: softer saturation
                    # alpha increases as v gets more negative
                    alpha = int((abs(v) / 2) * 100) # Max 100 for pastel feel
                    return f'background-color: rgb(255, {255-alpha}, {255-alpha})'
                else:
                    # Pastel Blue for positive: softer saturation
                    alpha = int((v / 2) * 100) # Max 100 for pastel feel
                    return f'background-color: rgb({255-alpha}, {255-alpha}, 255)'

            styled_coef = coef_df.style.map(color_scale).format("{:.3f}")
            
            coef_pane.append(pn.pane.HTML("<h3 style='color: #2c3e50;'>Tabel Koefisien Regresi Logistik per Kelas</h3>"))
            coef_pane.append(pn.pane.DataFrame(styled_coef, sizing_mode='stretch_width'))
            coef_pane.append(pn.pane.HTML("""
                <div style="background-color: #f8f9fa; border-left: 5px solid #007bff; padding: 15px; border-radius: 4px; margin-top: 15px;">
                    <p style="margin: 0; color: #495057;">
                        <strong>Keterangan:</strong> Semakin besar nilai mutlaknya, maka semakin kuat pengaruh variabel itu ada di tipe booth tertentu. 
                        Jika nilai negatif, maka memperkecil kemungkinan di booth itu. Jika nilai positif, maka memperbesar kemungkinannya. 
                        Jika nilai 0, maka tidak ada pengaruh (karena hasil regularisasi).
                    </p>
                </div>
            """, sizing_mode='stretch_width'))
        else:
            coef_pane.append(pn.pane.Markdown("*Tabel koefisien tidak tersedia dalam data importance.*"))
    except Exception as e:
        coef_pane.append(pn.pane.Markdown(f"*Error memproses koefisien:* {e}"))

    keterangan = pn.pane.HTML("""
        <div style="background-color: #f8f9fa; border-left: 5px solid #007bff; padding: 15px; border-radius: 4px; margin: 15px 0;">
            <p style="margin: 0; color: #495057;">
                <strong>Keterangan:</strong> Faktor pengaruh didapatkan dengan menghitung nilai mutlak rata-rata dari koefisien Regresi Logistik dengan regularisasi L1 (Lasso).
                Semakin tinggi nilainya, maka semakin besar dampaknya. Arah pengaruh secara detail dapat dilihat pada tabel koefisien di bawah ini.
            </p>
        </div>
    """, sizing_mode='stretch_width')

    feature_options = df_sorted.sort_values(by='Importance', ascending=False)['Feature'].tolist()
    feature_selector = pn.widgets.Select(name='🔍 Pilih Variabel untuk Diinspeksi', options=feature_options, sizing_mode='stretch_width')

    @pn.depends(feature_selector.param.value)
    def render_stacked_bars(selected_feature):
        if df is None or selected_feature not in df.columns:
            return pn.pane.Markdown(f"*Data kolom '{selected_feature}' tidak ditemukan.*")
        target_col = 'circle_type'
        df_valid = df.dropna(subset=[target_col, selected_feature]).copy()
        df_valid['Feature_Value'] = df_valid[selected_feature].astype(int).astype(str)
        # 1 Space: Blue, 2 Space: Green, 4 Space: Magenta (replaced orange), Booth A: Violet, Booth B: Red
        circle_color_map = {'1 Space(s)': '#3b82f6', '2 Space(s)': '#10b981', '4 Space(s)': '#d946ef', 'Booth_A': '#8b5cf6', 'Booth_B': '#ef4444'}
        
        counts1 = df_valid.groupby([target_col, 'Feature_Value']).size().reset_index(name='Count')
        fig1 = px.bar(counts1, y=target_col, x='Count', color='Feature_Value', orientation='h', title=f"Distribusi '{selected_feature}' per Tipe Booth", color_discrete_map={'1': '#f59e0b', '0': '#94a3b8'}, barmode='stack', category_orders={target_col: list(circle_color_map.keys()), 'Feature_Value': ['0', '1']})
        
        counts2 = df_valid.groupby(['Feature_Value', target_col]).size().reset_index(name='Count')
        fig2 = px.bar(counts2, y='Feature_Value', x='Count', color=target_col, orientation='h', title=f"Komposisi Tipe Booth pada '{selected_feature}'", color_discrete_map=circle_color_map, barmode='stack', category_orders={'Feature_Value': ['0', '1'], target_col: list(circle_color_map.keys())})
        
        return pn.Row(pn.pane.Plotly(fig1, sizing_mode="stretch_width", height=350), pn.pane.Plotly(fig2, sizing_mode="stretch_width", height=350), sizing_mode="stretch_width")

    return pn.Column(type_desc, plot_pane, keterangan, pn.layout.Divider(), coef_pane, pn.layout.Divider(), pn.pane.HTML("<h2 style='color: #2c3e50;'>Inspeksi Detail Faktor</h2>"), feature_selector, render_stacked_bars, sizing_mode="stretch_width")
