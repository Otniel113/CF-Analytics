import panel as pn
import plotly.express as px
import pandas as pd

def create_tab(df=None):
    if df is None:
        return pn.pane.Markdown("# EDA Area\n*Data not loaded.*", sizing_mode="stretch_width")

    # Split data by CF version
    df_cf21 = df[df['CF_Version'] == 21]
    df_cf22 = df[df['CF_Version'] == 22]

    total_21 = len(df_cf21)
    total_22 = len(df_cf22)

    # 1. Total Booths (Styled HTML Cards)
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

    # Utility Functions for Plotly Charts
    def create_pie_chart(data, title, names_col, values_col):
        fig = px.pie(data, values=values_col, names=names_col, hole=0.4,
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_traces(textposition='inside', textinfo='percent+value')
        fig.update_layout(margin=dict(t=30, b=0, l=0, r=0), title_text=title, title_x=0.5)
        return pn.pane.Plotly(fig, sizing_mode='stretch_width')

    def create_bar_chart(data, title, x_col, y_col, total_booths, color_theme='blue'):
        color = '#3b82f6' if color_theme == 'blue' else '#94a3b8'
        
        # Calculate percentages for display
        data = data.copy()
        data['pct'] = (data[x_col] / total_booths * 100).round(1)
        data['display_text'] = data.apply(lambda r: f"{int(r[x_col])} ({r['pct']}%)", axis=1)
        
        fig = px.bar(data, x=x_col, y=y_col, orientation='h', text='display_text')
        fig.update_traces(marker_color=color, textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
        # Added margin r=80 to ensure labels don't get cut off
        fig.update_layout(margin=dict(t=30, b=0, l=0, r=80), title_text=title, title_x=0.5, yaxis={'categoryorder':'total ascending'})
        return pn.pane.Plotly(fig, sizing_mode='stretch_width')

    # 2. Fandom Distribution
    fandom_cols = ['Hoyoverse', 'Vtuber', 'Other Gacha', 'V-Synth', 'Original', 'Other (Niche)']
    def get_fandom_data(subset, total):
        counts = subset[fandom_cols].sum().to_dict()
        df_fandom = pd.DataFrame(list(counts.items()), columns=['Fandom', 'Count'])
        # Filter out 0 counts to keep pie chart clean
        return df_fandom[df_fandom['Count'] > 0]

    fandom_tabs = pn.Tabs(
        ('CF22', create_bar_chart(get_fandom_data(df_cf22, total_22), "Fandom Distribution (CF22)", 'Count', 'Fandom', total_22, 'blue')),
        ('CF21', create_bar_chart(get_fandom_data(df_cf21, total_21), "Fandom Distribution (CF21)", 'Count', 'Fandom', total_21, 'gray')),
        margin=(10, 0)
    )

    # 3. Category Circle Booth Type, Rating, Day
    def get_cat_data(subset, col):
        counts = subset[col].value_counts().reset_index()
        counts.columns = [col, 'Count']
        return counts

    ctype_tabs = pn.Tabs(
        ('CF22', create_pie_chart(get_cat_data(df_cf22, 'circle_type'), "Circle Booth Type (CF22)", 'circle_type', 'Count')),
        ('CF21', create_pie_chart(get_cat_data(df_cf21, 'circle_type'), "Circle Booth Type (CF21)", 'circle_type', 'Count')),
        margin=(10, 0)
    )
    
    rating_tabs = pn.Tabs(
        ('CF22', create_pie_chart(get_cat_data(df_cf22, 'rating'), "Rating (CF22)", 'rating', 'Count')),
        ('CF21', create_pie_chart(get_cat_data(df_cf21, 'rating'), "Rating (CF21)", 'rating', 'Count')),
        margin=(10, 0)
    )
    
    day_tabs = pn.Tabs(
        ('CF22', create_pie_chart(get_cat_data(df_cf22, 'day'), "Day (CF22)", 'day', 'Count')),
        ('CF21', create_pie_chart(get_cat_data(df_cf21, 'day'), "Day (CF21)", 'day', 'Count')),
        margin=(10, 0)
    )

    # 4. Social Media Links
    link_cols = ['circle_facebook', 'circle_instagram', 'circle_twitter', 'circle_other_socials', 'marketplace_link']
    def get_links_data(subset):
        counts = subset[link_cols].apply(lambda col: (col.notnull() & (col.astype(str).str.strip() != "-")).sum())
        df_links = pd.DataFrame({'Social Media': counts.index, 'Count': counts.values})
        # Prettify labels
        mapping = {
            'circle_facebook': 'Facebook',
            'circle_instagram': 'Instagram',
            'circle_twitter': 'Twitter (X)',
            'circle_other_socials': 'Other Socials',
            'marketplace_link': 'Marketplace'
        }
        df_links['Social Media'] = df_links['Social Media'].map(mapping)
        return df_links

    links_tabs = pn.Tabs(
        ('CF22', create_bar_chart(get_links_data(df_cf22), "Provided Links (CF22)", 'Count', 'Social Media', total_22, 'blue')),
        ('CF21', create_bar_chart(get_links_data(df_cf21), "Provided Links (CF21)", 'Count', 'Social Media', total_21, 'gray')),
        margin=(10, 0)
    )

    # 5. What They Sell
    sells_cols = [col for col in df.columns if col.startswith('Sells')]
    def get_sells_data(subset):
        counts = subset[sells_cols].sum()
        df_sells = pd.DataFrame({'Category': counts.index, 'Count': counts.values})
        df_sells['Category'] = df_sells['Category'].str.replace('Sells_', '').str.replace('Sells', '').str.strip()
        return df_sells

    sells_tabs = pn.Tabs(
        ('CF22', create_bar_chart(get_sells_data(df_cf22), "Product Category Participation (CF22)", 'Count', 'Category', total_22, 'blue')),
        ('CF21', create_bar_chart(get_sells_data(df_cf21), "Product Category Participation (CF21)", 'Count', 'Category', total_21, 'gray')),
        margin=(10, 0)
    )

    # Layout Construction
    layout = pn.Column(
        pn.pane.HTML("<h2 style='color: #2c3e50; border-bottom: 2px solid #007bff; padding-bottom: 10px; margin-bottom: 20px;'>Exploratory Data Analysis</h2>"),
        total_booths_pane,
        pn.layout.Divider(),
        pn.Row(
            pn.Column(pn.pane.HTML("<h3 style='text-align: center;'>Fandom Distribution</h3>"), fandom_tabs, sizing_mode='stretch_width', css_classes=['col-12', 'col-lg-6']),
            pn.Column(pn.pane.HTML("<h3 style='text-align: center;'>Circle Type</h3>"), ctype_tabs, sizing_mode='stretch_width', css_classes=['col-12', 'col-lg-6']),
            css_classes=['row']
        ),
        pn.Row(
            pn.Column(pn.pane.HTML("<h3 style='text-align: center;'>Rating</h3>"), rating_tabs, sizing_mode='stretch_width', css_classes=['col-12', 'col-lg-6']),
            pn.Column(pn.pane.HTML("<h3 style='text-align: center;'>Day</h3>"), day_tabs, sizing_mode='stretch_width', css_classes=['col-12', 'col-lg-6']),
            css_classes=['row']
        ),
        pn.layout.Divider(),
        pn.Row(
            pn.Column(pn.pane.HTML("<h3 style='text-align: center;'>Social Media & Links</h3>"), links_tabs, sizing_mode='stretch_width', css_classes=['col-12', 'col-lg-6']),
            pn.Column(pn.pane.HTML("<h3 style='text-align: center;'>What They Sell</h3>"), sells_tabs, sizing_mode='stretch_width', css_classes=['col-12', 'col-lg-6']),
            css_classes=['row']
        ),
        sizing_mode="stretch_width",
        margin=(20, 20)
    )
    
    return layout
