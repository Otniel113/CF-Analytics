import panel as pn
import plotly.express as px
import pandas as pd

def create_tab(df=None):
    if df is None:
        return pn.pane.Markdown("# Trend Analysis Area\n*Data not loaded.*", sizing_mode="stretch_width")

    # Split data by CF version for Total Booths
    df_cf21 = df[df['CF_Version'] == 21]
    df_cf22 = df[df['CF_Version'] == 22]

    total_21 = len(df_cf21)
    total_22 = len(df_cf22)

    # 1. Total Booths (Styled HTML Cards, exactly like EDA tab)
    total_booths_html = f"""
    <div style="display: flex; gap: 20px; justify-content: center; margin-bottom: 20px; flex-wrap: wrap;">
        <div style="background-color: #f8f9fa; border-left: 6px solid #3b82f6; padding: 20px; border-radius: 8px; width: 300px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h3 style="margin: 0; color: #495057;">Total Booths CF22</h3>
            <p style="font-size: 2.5rem; font-weight: bold; color: #3b82f6; margin: 10px 0 0 0;">{total_22}</p>
        </div>
        <div style="background-color: #f8f9fa; border-left: 6px solid #94a3b8; padding: 20px; border-radius: 8px; width: 300px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h3 style="margin: 0; color: #495057;">Total Booths CF21</h3>
            <p style="font-size: 2.5rem; font-weight: bold; color: #94a3b8; margin: 10px 0 0 0;">{total_21}</p>
        </div>
    </div>
    """
    total_booths_pane = pn.pane.HTML(total_booths_html, sizing_mode='stretch_width')

    # 2. Data Preparation for Fandom Trends
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

    # 3. Line Plots
    # Custom color mapping to match standard fandom colors
    color_map = {
        'Hoyoverse': '#3b82f6',
        'Vtuber': '#8b5cf6',
        'Other Gacha': '#f59e0b',
        'V-Synth': '#2dd4bf',
        'Original': '#db2777',
        'Other (Niche)': '#64748b'
    }

    # Plot 1: Trend by Percentage
    fig_pct = px.line(df_trend, x='Event', y='Percentage', color='Fandom', markers=True,
                      color_discrete_map=color_map)
    fig_pct.update_traces(line=dict(width=3), marker=dict(size=10))
    fig_pct.update_layout(
        title="Market Share Comparison: Fandom Categories (CF21 vs CF22)",
        title_x=0.5,
        yaxis_title="Percentage of Total Booths (%)",
        xaxis_title="Event",
        margin=dict(t=50, b=30, l=30, r=30),
        yaxis=dict(range=[0, df_trend['Percentage'].max() + 10]) # Add some headroom
    )
    pane_pct = pn.pane.Plotly(fig_pct, sizing_mode='stretch_width', min_height=500)

    # Plot 2: Trend by Absolute Count
    fig_count = px.line(df_trend, x='Event', y='Count', color='Fandom', markers=True,
                        color_discrete_map=color_map)
    fig_count.update_traces(line=dict(width=3), marker=dict(size=10))
    fig_count.update_layout(
        title="Booth Count Comparison: Fandom Categories (CF21 vs CF22)",
        title_x=0.5,
        yaxis_title="Number of Booths",
        xaxis_title="Event",
        margin=dict(t=50, b=30, l=30, r=30),
        yaxis=dict(range=[0, df_trend['Count'].max() + 50]) # Add some headroom
    )
    pane_count = pn.pane.Plotly(fig_count, sizing_mode='stretch_width', min_height=500)

    # 4. Assemble the layout
    layout = pn.Column(
        pn.pane.HTML("<h2 style='color: #2c3e50; border-bottom: 2px solid #007bff; padding-bottom: 10px; margin-bottom: 20px;'>Trend Analysis</h2>"),
        total_booths_pane,
        pn.layout.Divider(),
        pn.Row(
            pn.Column(pane_pct, sizing_mode='stretch_width'),
            pn.Column(pane_count, sizing_mode='stretch_width')
        ),
        sizing_mode="stretch_width",
        margin=(20, 20)
    )
    
    return layout
