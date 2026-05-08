import panel as pn
import pandas as pd

def filter_data(df, search, sells, links, fandoms, circle_type, rating, day, cf_version):
    # Filter by CF_Version immediately
    filtered_df = df[df['CF_Version'] == cf_version].copy()
    
    # Text Search (Code, Name, Fandoms)
    if search:
        search = search.lower()
        mask = (
            filtered_df['circle_code'].str.lower().str.contains(search, na=False) |
            filtered_df['name'].str.lower().str.contains(search, na=False) |
            filtered_df['fandom'].str.lower().str.contains(search, na=False) |
            filtered_df['other_fandom'].str.lower().str.contains(search, na=False)
        )
        filtered_df = filtered_df[mask]
        
    # Checkbox Filters (Requires ALL checked boxes to be True / Not Null)
    for sell_item in sells:
        filtered_df = filtered_df[filtered_df[sell_item] == True]
        
    for link_item in links:
        filtered_df = filtered_df[filtered_df[link_item].notna() & (filtered_df[link_item].astype(str).str.strip() != "-")]
        
    for fandom_item in fandoms:
        filtered_df = filtered_df[filtered_df[fandom_item] == True]
        
    # Dropdown Filters
    if circle_type != 'All': 
        filtered_df = filtered_df[filtered_df['circle_type'] == circle_type]
    if rating != 'All': 
        filtered_df = filtered_df[filtered_df['rating'] == rating]
    if day != 'All': 
        filtered_df = filtered_df[filtered_df['day'] == day]
        
    # Determine columns for reordering
    base_cols = ['circle_code', 'name', 'fandom', 'other_fandom', 'circle_type', 'day', 'rating']
    social_cols = ['circle_facebook', 'circle_instagram', 'circle_twitter', 'circle_other_socials', 'marketplace_link']
    sell_cols = [col for col in filtered_df.columns if col.startswith('Sells')]
    fan_cols = [col for col in ['Hoyoverse', 'Vtuber', 'Other Gacha', 'V-Synth', 'Original', 'Other (Niche)'] if col in filtered_df.columns]
    
    # Rename columns for clarity (optional, but requested columns reorder)
    ordered_cols = [col for col in base_cols + social_cols + sell_cols + fan_cols if col in filtered_df.columns]
    # Add any remaining hidden columns or others at the end
    missing_cols = [col for col in filtered_df.columns if col not in ordered_cols]
    filtered_df = filtered_df[ordered_cols + missing_cols]
    
    # Formatting expected Boolean columns (0/1 or True/False or string 0/1) to Yes/No for user
    bool_cols_to_map = sell_cols + fan_cols
    for col in bool_cols_to_map:
        filtered_df[col] = filtered_df[col].map({1: 'Yes', 0: 'No', 1.0: 'Yes', 0.0: 'No', True: 'Yes', False: 'No', '1': 'Yes', '0': 'No', '1.0': 'Yes', '0.0': 'No'}).fillna('No')
        
    # Drop CF_Version for user
    if 'CF_Version' in filtered_df.columns:
        filtered_df = filtered_df.drop(columns=['CF_Version'])
        
    # Add No. column starting from 1
    filtered_df = filtered_df.reset_index(drop=True)
    filtered_df.index += 1
    filtered_df.insert(0, 'No.', filtered_df.index)
    
    return filtered_df

def create_tab(df):
    # ==========================================
    # DEFINE WIDGETS (Filters)
    # ==========================================
    search_input = pn.widgets.TextInput(name='Search', placeholder='Search Code, Name, or Fandom...')

    # Filters 1, 2, 3: Selects
    circle_type_filter = pn.widgets.Select(name='Circle Type', options=['All'] + sorted(df['circle_type'].dropna().unique().tolist()))
    rating_filter = pn.widgets.Select(name='Rating', options=['All'] + sorted(df['rating'].dropna().unique().tolist()))
    day_filter = pn.widgets.Select(name='Day', options=['All'] + sorted(df['day'].dropna().unique().tolist()))

    # Filter 4: Sells (Split into two columns as requested)
    sells_cols = [c for c in df.columns if c.startswith('Sells')]
    sells_options = {c.replace('Sells_', '').replace('Sells', '').strip(): c for c in sells_cols}
    items = list(sells_options.items())
    mid = 6 # User specifically asked for 6 and 5 split
    sells_filter_1 = pn.widgets.CheckBoxGroup(options=dict(items[:mid]))
    sells_filter_2 = pn.widgets.CheckBoxGroup(options=dict(items[mid:]))
    combined_sells = pn.bind(lambda s1, s2: list(s1) + list(s2), sells_filter_1, sells_filter_2)

    # Filter 5: Links
    link_options = {
        'Facebook': 'circle_facebook',
        'Instagram': 'circle_instagram',
        'Twitter (X)': 'circle_twitter',
        'Other Socials': 'circle_other_socials',
        'Marketplace': 'marketplace_link'
    }
    link_filter = pn.widgets.CheckBoxGroup(options=link_options)

    # Filter 6: Fandom
    fandom_cols = ['Hoyoverse', 'Vtuber', 'Other Gacha', 'V-Synth', 'Original', 'Other (Niche)']
    # Filter only matching columns that exist in the dataframe
    fandom_cols = [c for c in fandom_cols if c in df.columns]
    fandom_filter = pn.widgets.CheckBoxGroup(options=fandom_cols)

    # ==========================================
    # BIND DATA TO TABLES
    # ==========================================
    # We create two reactive datasets, one for CF21, one for CF22
    df_cf21 = pn.bind(filter_data, df, search_input, combined_sells, link_filter, fandom_filter, circle_type_filter, rating_filter, day_filter, 21)
    df_cf22 = pn.bind(filter_data, df, search_input, combined_sells, link_filter, fandom_filter, circle_type_filter, rating_filter, day_filter, 22)

    # Create highly performant Tabulator widgets
    hidden_cols = ['id', 'user_id', 'circle_cut', 'sampleworks_images']

    # Load external CSS for Tabulator styling
    css_path = 'assets/css/style.css'

    # Page size selector
    page_size_selector = pn.widgets.Select(name='Show rows', options=[10, 25, 50], value=10, width=120)

    table_cf21 = pn.widgets.Tabulator(df_cf21, pagination='remote', page_size=10, hidden_columns=hidden_cols, disabled=True, stylesheets=[css_path], theme='bootstrap5', show_index=False)
    table_cf22 = pn.widgets.Tabulator(df_cf22, pagination='remote', page_size=10, hidden_columns=hidden_cols, disabled=True, stylesheets=[css_path], theme='bootstrap5', show_index=False)


    page_size_selector.link(table_cf21, value='page_size')
    page_size_selector.link(table_cf22, value='page_size')

    # ==========================================
    # BUILD THE UI LAYOUT
    # ==========================================
    # Group filters into containers with matching background colors
    search_block = pn.Column(
        search_input,
        margin=(10, 0, 25, 0),
        styles={'padding': '15px'},
        sizing_mode="stretch_width"
    )
    general_block = pn.Column(
        "**General Filters**", 
        pn.Row(circle_type_filter, rating_filter, day_filter, sizing_mode="stretch_width"), 
        styles={'background': '#B0E0E6', 'padding': '10px', 'border-radius': '8px'},
        sizing_mode="stretch_width"
    )

    sells_block = pn.Column(
        "**What they Sell**", 
        pn.Row(sells_filter_1, sells_filter_2, sizing_mode="stretch_width"), 
        styles={'background': '#f8d7da', 'padding': '10px', 'border-radius': '8px', 'min_height': '200px'},
        sizing_mode="stretch_both"
    )
    social_block = pn.Column(
        "**Social / Links**", link_filter, 
        styles={'background': '#a3e4af', 'padding': '10px', 'border-radius': '8px', 'min_height': '200px'},
        sizing_mode="stretch_both"
    )
    fandom_block = pn.Column(
        "**Fandom Focus**", fandom_filter, 
        styles={'background': '#fff3cd', 'padding': '10px', 'border-radius': '8px', 'min_height': '200px'},
        sizing_mode="stretch_both"
    )

    # Row 1: Search and General
    row1 = pn.Row(search_block, general_block, sizing_mode="stretch_width")

    # Row 2: Sells (2 cols), Social (1 col), Fandom (1 col)
    # We use flex styles to give Sells more space (2:1:1 ratio)
    row2 = pn.Row(
        pn.Column(social_block, styles={'flex': '1'}),
        pn.Column(sells_block, styles={'flex': '2'}),
        pn.Column(fandom_block, styles={'flex': '1'}),
        sizing_mode="stretch_width"
    )

    tab_stylesheet = """
    .bk-tab {
        font-size: 1.1rem !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease;
        border-radius: 8px 8px 0 0 !important;
    }
    .bk-tab:hover {
        background-color: #f8f9fa !important;
        color: #007bff !important;
    }
    .bk-tab.bk-active {
        color: #007bff !important;
        border-bottom: 4px solid #007bff !important;
        background-color: #ffffff !important;
    }
    """


    # The inner tabs for CF21 vs CF22 tables
    master_data_subtabs = pn.Tabs(
        ('CF22', table_cf22),
        ('CF21', table_cf21),
        stylesheets=[tab_stylesheet],
        margin=(20, 0)
    )

    # Table controls placed at the top right
    table_controls = pn.Row(
        pn.layout.HSpacer(),
        page_size_selector,
        sizing_mode="stretch_width",
        margin=(10, 0, 5, 0)
    )

    # Combine everything into one column
    return pn.Column(row1, row2, table_controls, master_data_subtabs, margin=(0, 0, 80, 0))
