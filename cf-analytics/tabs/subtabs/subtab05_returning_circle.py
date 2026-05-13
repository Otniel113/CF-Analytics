import panel as pn
import plotly.express as px
import pandas as pd

def create_returning_circle_subtab(df, df_returning):
    if df_returning is None:
        return pn.pane.Markdown("*Returning Circle data not found.*")

    # Calculate totals from df for comparison
    df_cf21 = df[df['CF_Version'] == 21]
    df_cf22 = df[df['CF_Version'] == 22]
    total_21 = len(df_cf21)
    total_22 = len(df_cf22)

    num_returning = len(df_returning)
    pct_cf21 = (num_returning / total_21 * 100) if total_21 > 0 else 0
    pct_cf22 = (num_returning / total_22 * 100) if total_22 > 0 else 0
    
    disclaimer = pn.pane.Markdown(
        "> **Disclaimer**: Angka asli returning circle (sirkel yang hadir kembali) kemungkinan lebih tinggi. Data ini hanya menghitung sirkel yang menggunakan nama (name) sama persis. Jika ada typo ataupun beda ejaan ataupun beda nama, maka tidak dihitung.",
        styles={'color': '#856404', 'background-color': '#fff3cd', 'padding': '15px', 'border-radius': '8px', 'border-left': '5px solid #ffeeba'},
        sizing_mode="stretch_width"
    )
    
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

    ret_info_html = f"""
    <div style="display: flex; gap: 20px; justify-content: center; margin-bottom: 20px; flex-wrap: wrap;">
        <div style="background-color: #f8f9fa; border-left: 6px solid #10b981; padding: 20px; border-radius: 8px; width: 250px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h3 style="margin: 0; color: #495057; font-size: 1rem;">Total Returning Circles</h3>
            <p style="font-size: 2rem; font-weight: bold; color: #10b981; margin: 10px 0 0 0;">{num_returning}</p>
        </div>
        <div style="background-color: #f8f9fa; border-left: 6px solid #6366f1; padding: 20px; border-radius: 8px; width: 250px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h3 style="margin: 0; color: #495057; font-size: 1rem;">% of CF22 Booths</h3>
            <p style="font-size: 2rem; font-weight: bold; color: #6366f1; margin: 10px 0 0 0;">{pct_cf22:.1f}%</p>
        </div>
        <div style="background-color: #f8f9fa; border-left: 6px solid #8b5cf6; padding: 20px; border-radius: 8px; width: 250px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h3 style="margin: 0; color: #495057; font-size: 1rem;">% of CF21 Booths</h3>
            <p style="font-size: 2rem; font-weight: bold; color: #8b5cf6; margin: 10px 0 0 0;">{pct_cf21:.1f}%</p>
        </div>
    </div>
    """
    ret_info_pane = pn.pane.HTML(ret_info_html, sizing_mode='stretch_width')
    
    # Color palettes for pies
    pie_colors = {
        'Upgrade': '#2ecc71', 'Downgrade': '#e74c3c', 'Stay': '#f1c40f',
        'Expander': '#2ecc71', 'Karbit': '#e74c3c', 'Loyalist': '#f1c40f',
        'More Diverse': '#2ecc71', 'Less Diverse': '#e74c3c',
        'Incomplete': '#95a5a6', 'Other': '#95a5a6'
    }
    
    # Pie 1: Upgrade Status
    upgrade_counts = df_returning['upgrade_status'].value_counts().reset_index()
    upgrade_counts.columns = ['Status', 'Count']
    fig_upg = px.pie(upgrade_counts, values='Count', names='Status', hole=0.4,
                     color='Status', color_discrete_map=pie_colors,
                     title="Circle Booth Type Upgrade Status")
    fig_upg.update_layout(margin=dict(t=50, b=30, l=10, r=10), title_x=0.5)
    pane_upg = pn.pane.Plotly(fig_upg, sizing_mode='stretch_width', min_height=400)
    desc_upg = pn.pane.Markdown("<p style='text-align:center; color:#6c757d; font-size:0.95rem; padding:0 20px;'>Mencari tahu apakah returning circle melakukan upgrade tipe circle booth atau tidak. Urutannya dari yang paling 'mewah' sampai 'sederhana' adalah Booth B > Booth A = 4 Space > 2 Space > 1 Space</p>")
    
    # Pie 2: Karbit Detection
    karbit_counts = df_returning['fandom_loyalty'].value_counts().reset_index()
    karbit_counts.columns = ['Status', 'Count']
    fig_karbit = px.pie(karbit_counts, values='Count', names='Status', hole=0.4,
                        color='Status', color_discrete_map=pie_colors,
                        title="Karbit Detection")
    fig_karbit.update_layout(margin=dict(t=50, b=30, l=10, r=10), title_x=0.5)
    pane_karbit = pn.pane.Plotly(fig_karbit, sizing_mode='stretch_width', min_height=400)
    desc_karbit = pn.pane.Markdown("""<div style='color:#6c757d; font-size:0.95rem; padding:0 20px;'>
Mencari tahu apakah returning circle adalah fandom karbit atau bukan. Ada 3 kategori:<br>
- <b>Loyalist</b> = Jika kategori fandom sama persis dari CF sebelumnya<br>
- <b>Karbit</b> = Jika di CF sebelumnya adalah fandom tertentu, tapi di CF terbaru malah tidak masuk ke fandom itu lagi<br>
- <b>Expander</b> = Jika kategori fandom sama dengan CF sebelumnya, namun juga ikut masuk atau menbambah fandom
</div>""")
    
    # Pie 3: Product Diversification
    diver_counts = df_returning['diver_status'].value_counts().reset_index()
    diver_counts.columns = ['Status', 'Count']
    fig_diver = px.pie(diver_counts, values='Count', names='Status', hole=0.4,
                       color='Status', color_discrete_map=pie_colors,
                       title="Product Diversification")
    fig_diver.update_layout(margin=dict(t=50, b=30, l=10, r=10), title_x=0.5)
    pane_diver = pn.pane.Plotly(fig_diver, sizing_mode='stretch_width', min_height=400)
    desc_diver = pn.pane.Markdown("<p style='text-align:center; color:#6c757d; font-size:0.95rem; padding:0 20px;'>Mencari tahu banyaknya jumlah jenis produk yang dijual. Didapatkan dengan menghitung total kolom 'Sells'. Memiliki 3 kategori: Less Diverse (CF terbaru jenis produk lebih sedikit), Stay (jenis produk sama), More Diverse (jenis produk makin bertambah)</p>")

    # Table for df_returning
    search_input_ret = pn.widgets.TextInput(name='Search by Circle Name', placeholder='Enter circle name...')
    filter_upgrade = pn.widgets.Select(name='Filter by Upgrade Status', options=['All'] + list(df_returning['upgrade_status'].dropna().unique()), value='All')
    filter_fandom = pn.widgets.Select(name='Filter by Fandom Loyalty', options=['All'] + list(df_returning['fandom_loyalty'].dropna().unique()), value='All')
    filter_diver = pn.widgets.Select(name='Filter by Product Diversification', options=['All'] + list(df_returning['diver_status'].dropna().unique()), value='All')
    
    page_size_selector_ret = pn.widgets.Select(name='Show rows', options=[10, 25, 50], value=10, width=120)
    
    def filter_returning(df_ret, search_query, upgrade_val, fandom_val, diver_val):
        filtered = df_ret.copy()
        if search_query:
            filtered = filtered[filtered['name'].str.contains(search_query, case=False, na=False)]
        if upgrade_val != 'All':
            filtered = filtered[filtered['upgrade_status'] == upgrade_val]
        if fandom_val != 'All':
            filtered = filtered[filtered['fandom_loyalty'] == fandom_val]
        if diver_val != 'All':
            filtered = filtered[filtered['diver_status'] == diver_val]
        filtered.reset_index(drop=True, inplace=True)
        filtered.index += 1
        filtered.insert(0, 'No.', filtered.index)
        return filtered

    interactive_returning = pn.bind(filter_returning, df_returning, search_input_ret, filter_upgrade, filter_fandom, filter_diver)
    
    ret_table = pn.widgets.Tabulator(
        interactive_returning,
        pagination='remote',
        page_size=10,
        theme='bootstrap5',
        layout='fit_data_stretch',
        sizing_mode='stretch_width',
        show_index=False,
        header_align='center',
        text_align='left',
        disabled=True
    )
    
    page_size_selector_ret.link(ret_table, value='page_size')
    
    return pn.Column(
        disclaimer,
        total_booths_pane,
        ret_info_pane,
        pn.layout.Divider(),
        pn.FlexBox(
            pn.Column(pane_upg, desc_upg, min_width=300, sizing_mode='stretch_width'),
            pn.Column(pane_karbit, desc_karbit, min_width=300, sizing_mode='stretch_width'),
            pn.Column(pane_diver, desc_diver, min_width=300, sizing_mode='stretch_width')
        ),
        pn.layout.Divider(),
        pn.pane.HTML("<h3 style='color: #495057; margin-bottom: 15px;'>Returning Circles Data</h3>"),
        pn.FlexBox(search_input_ret, filter_upgrade, filter_fandom, filter_diver, page_size_selector_ret, sizing_mode='stretch_width'),
        ret_table,
        sizing_mode='stretch_width'
    )
