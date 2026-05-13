import panel as pn
import plotly.express as px
import pandas as pd

def create_fandom_trend_subtab(df):
    if df is None:
        return pn.pane.Markdown("*Data not loaded.*")

    # ==========================================
    # DATA PREPARATION: TOTAL BOOTHS
    # ==========================================
    df_cf21 = df[df['CF_Version'] == 21]
    df_cf22 = df[df['CF_Version'] == 22]

    total_21 = len(df_cf21)
    total_22 = len(df_cf22)

    total_booths_html = f"""
    <div style="display: flex; gap: 20px; justify-content: center; margin-bottom: 30px; flex-wrap: wrap;">
        <div style="background-color: #f8f9fa; border-left: 8px solid #3b82f6; padding: 25px; border-radius: 12px; width: 350px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
            <h3 style="margin: 0; color: #495057; font-size: 1.2rem;">Total Booths CF22</h3>
            <p style="font-size: 3rem; font-weight: bold; color: #3b82f6; margin: 10px 0 0 0;">{total_22}</p>
        </div>
        <div style="background-color: #f8f9fa; border-left: 8px solid #94a3b8; padding: 25px; border-radius: 12px; width: 350px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
            <h3 style="margin: 0; color: #495057; font-size: 1.2rem;">Total Booths CF21</h3>
            <p style="font-size: 3rem; font-weight: bold; color: #94a3b8; margin: 10px 0 0 0;">{total_21}</p>
        </div>
    </div>
    """
    total_booths_pane = pn.pane.HTML(total_booths_html, sizing_mode='stretch_width')

    # ==========================================
    # DATA PREPARATION: FANDOM CATEGORIES
    # ==========================================
    fandom_cols = ['Hoyoverse', 'Vtuber', 'Other Gacha', 'V-Synth', 'Original', 'Other (Niche)']
    summary_data = []
    for cf_ver in [21, 22]:
        subset = df[df['CF_Version'] == cf_ver]
        total = len(subset)
        counts = subset[fandom_cols].sum()
        for fandom in fandom_cols:
            count = counts[fandom]
            pct = (count / total) * 100
            summary_data.append({
                'Event': f'CF{cf_ver}',
                'Fandom': fandom,
                'Count': count,
                'Percentage': pct
            })
    df_trend = pd.DataFrame(summary_data)

    color_map = {
        'Hoyoverse': '#3b82f6',
        'Vtuber': '#8b5cf6',
        'Other Gacha': '#f59e0b',
        'V-Synth': '#2dd4bf',
        'Original': '#db2777',
        'Other (Niche)': '#64748b'
    }

    fig_pct = px.line(df_trend, x='Event', y='Percentage', color='Fandom', markers=True, color_discrete_map=color_map)
    fig_pct.update_traces(line=dict(width=4), marker=dict(size=12))
    fig_pct.update_layout(
        title="Market Share Comparison: Fandom Categories",
        title_x=0.5,
        yaxis_title="Percentage (%)",
        xaxis_title="Event",
        margin=dict(t=60, b=30, l=30, r=30),
        yaxis=dict(range=[0, df_trend['Percentage'].max() + 10])
    )
    pane_pct = pn.pane.Plotly(fig_pct, sizing_mode='stretch_width', min_height=500, styles={'flex': '1 1 45%'}, min_width=350)

    fig_count = px.line(df_trend, x='Event', y='Count', color='Fandom', markers=True, color_discrete_map=color_map)
    fig_count.update_traces(line=dict(width=4), marker=dict(size=12))
    fig_count.update_layout(
        title="Booth Count Comparison: Fandom Categories",
        title_x=0.5,
        yaxis_title="Number of Booths",
        xaxis_title="Event",
        margin=dict(t=60, b=30, l=30, r=30),
        yaxis=dict(range=[0, df_trend['Count'].max() + 50])
    )
    pane_count = pn.pane.Plotly(fig_count, sizing_mode='stretch_width', min_height=500, styles={'flex': '1 1 45%'}, min_width=350)

    # ==========================================
    # SPECIFIC FANDOM SEARCH (ENHANCED/BIGGER)
    # ==========================================
    search_title = pn.pane.HTML("<h2 style='margin-top: 40px; color: #1e293b; border-left: 8px solid #3b82f6; padding-left: 20px; font-size: 2rem;'>Pencarian Trend Fandom Spesifik</h2>")
    search_description = pn.pane.Markdown(
        "### Ingin mencari fandom spesifik lainnya? \n"
        "Cari di sini untuk melihat perkembangannya dari CF sebelumnya.",
        styles={'font-size': '1.2rem', 'color': '#475569', 'margin-bottom': '20px'}
    )

    fandom_search_input = pn.widgets.TextInput(
        name='Masukkan Nama Fandom', 
        placeholder='Contoh: Naruto, One Piece, Ghibli, Arknight, Fate, ...',
        sizing_mode='stretch_width',
        styles={'font-size': '1.3rem', 'font-weight': 'bold'}
    )

    @pn.depends(f_search=fandom_search_input.param.value)
    def get_fandom_search_results(f_search):
        if not f_search or len(f_search) < 2:
            return pn.pane.Alert("### Silakan ketik nama fandom (minimal 2 karakter) untuk memulai analisis spesifik.", alert_type="info")
        
        f_search_lower = f_search.lower()
        mask = (
            df['fandom'].str.lower().str.contains(f_search_lower, na=False) |
            df['other_fandom'].str.lower().str.contains(f_search_lower, na=False)
        )
        df_fandom = df[mask]
        
        if df_fandom.empty:
            return pn.pane.Alert(f"### Tidak ada data ditemukan untuk fandom: **{f_search}**", alert_type="warning")

        df_f_21 = df_fandom[df_fandom['CF_Version'] == 21]
        df_f_22 = df_fandom[df_fandom['CF_Version'] == 22]
        
        f_count_21 = len(df_f_21)
        f_count_22 = len(df_f_22)
        
        total_21_all = len(df[df['CF_Version'] == 21])
        total_22_all = len(df[df['CF_Version'] == 22])
        
        f_pct_21 = (f_count_21 / total_21_all * 100) if total_21_all > 0 else 0
        f_pct_22 = (f_count_22 / total_22_all * 100) if total_22_all > 0 else 0
        
        growth_count = f_count_22 - f_count_21
        growth_color = "#10b981" if growth_count >= 0 else "#ef4444"
        
        search_metrics_html = f"""
        <div style="display: flex; gap: 20px; justify-content: center; margin: 30px 0; flex-wrap: wrap;">
            <div style="background-color: #ffffff; border-top: 6px solid #3b82f6; padding: 25px; border-radius: 12px; width: 250px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); text-align: center;">
                <h4 style="margin: 0; color: #64748b; font-size: 1rem; text-transform: uppercase; letter-spacing: 1px;">Booth CF22</h4>
                <p style="font-size: 2.5rem; font-weight: bold; color: #3b82f6; margin: 10px 0;">{f_count_22}</p>
                <p style="margin: 0; color: #1e293b; font-size: 1.2rem; font-weight: 500;">{f_pct_22:.2f}% <span style="font-size: 0.9rem; color: #64748b; font-weight: 400;">share</span></p>
            </div>
            <div style="background-color: #ffffff; border-top: 6px solid #94a3b8; padding: 25px; border-radius: 12px; width: 250px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); text-align: center;">
                <h4 style="margin: 0; color: #64748b; font-size: 1rem; text-transform: uppercase; letter-spacing: 1px;">Booth CF21</h4>
                <p style="font-size: 2.5rem; font-weight: bold; color: #94a3b8; margin: 10px 0;">{f_count_21}</p>
                <p style="margin: 0; color: #1e293b; font-size: 1.2rem; font-weight: 500;">{f_pct_21:.2f}% <span style="font-size: 0.9rem; color: #64748b; font-weight: 400;">share</span></p>
            </div>
            <div style="background-color: #ffffff; border-top: 6px solid {growth_color}; padding: 25px; border-radius: 12px; width: 250px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); text-align: center;">
                <h4 style="margin: 0; color: #64748b; font-size: 1rem; text-transform: uppercase; letter-spacing: 1px;">Pertumbuhan</h4>
                <p style="font-size: 2.5rem; font-weight: bold; color: {growth_color}; margin: 10px 0;">{"+" if growth_count >= 0 else ""}{growth_count}</p>
                <p style="margin: 0; color: #1e293b; font-size: 1.2rem; font-weight: 500;">{"+" if f_pct_22 - f_pct_21 >= 0 else ""}{f_pct_22 - f_pct_21:.2f}% <span style="font-size: 0.9rem; color: #64748b; font-weight: 400;">pts</span></p>
            </div>
        </div>
        """
        
        f_trend_data = pd.DataFrame([
            {'Event': 'CF21', 'Count': f_count_21, 'Percentage': f_pct_21},
            {'Event': 'CF22', 'Count': f_count_22, 'Percentage': f_pct_22}
        ])
        
        fig_f_pct = px.line(f_trend_data, x='Event', y='Percentage', markers=True, color_discrete_sequence=['#8b5cf6'])
        fig_f_pct.update_traces(line=dict(width=5), marker=dict(size=14))
        fig_f_pct.update_layout(title=f"Market Share Trend: {f_search}", yaxis_title="Percentage (%)", height=400, margin=dict(t=60, b=30, l=30, r=30))
        
        fig_f_count = px.line(f_trend_data, x='Event', y='Count', markers=True, color_discrete_sequence=['#3b82f6'])
        fig_f_count.update_traces(line=dict(width=5), marker=dict(size=14))
        fig_f_count.update_layout(title=f"Booth Count Trend: {f_search}", yaxis_title="Booths", height=400, margin=dict(t=60, b=30, l=30, r=30))
        
        return pn.Column(
            pn.pane.HTML(search_metrics_html, sizing_mode='stretch_width'),
            pn.FlexBox(
                pn.pane.Plotly(fig_f_pct, sizing_mode='stretch_width', min_width=350, styles={'flex': '1 1 45%'}),
                pn.pane.Plotly(fig_f_count, sizing_mode='stretch_width', min_width=350, styles={'flex': '1 1 45%'}),
                sizing_mode='stretch_width',
                justify_content='center'
            ),
            sizing_mode='stretch_width'
        )

    search_section = pn.Column(
        search_title,
        search_description,
        fandom_search_input,
        get_fandom_search_results,
        styles={'background': '#f1f5f9', 'padding': '40px', 'border-radius': '20px', 'margin-top': '40px'},
        sizing_mode="stretch_width"
    )

    return pn.Column(
        total_booths_pane,
        pn.layout.Divider(),
        pn.FlexBox(
            pane_pct,
            pane_count,
            sizing_mode='stretch_width',
            justify_content='center'
        ),
        pn.layout.Divider(),
        search_section,
        sizing_mode="stretch_width",
        margin=(10, 0)
    )
