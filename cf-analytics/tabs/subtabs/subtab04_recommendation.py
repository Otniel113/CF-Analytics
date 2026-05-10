import panel as pn
import pandas as pd
import numpy as np
import joblib
import os
from scipy.spatial.distance import cdist

class CircleRecommender:
    def __init__(self):
        pass

    def prepare_raw_data(self, df_raw):
        sells_cols = [col for col in df_raw.columns if col.startswith('Sells')]
        last_6_cols = df_raw.columns[-6:].tolist()
        other_cols = ['name', 'circle_code', 'CF_Version', 'rating', 'day', 'circle_type']

        selected_columns = []
        for col in (other_cols + sells_cols + last_6_cols):
            if col in df_raw.columns and col not in selected_columns:
                selected_columns.append(col)

        df = df_raw[selected_columns].copy()

        # One-Hot Encoding
        df = pd.get_dummies(df, columns=['rating', 'day', 'circle_type'],
                            prefix=['rating', 'day', 'circle_type'])

        # Split by CF_Version and drop version column
        df_21 = df[df['CF_Version'] == 21].drop(columns=['CF_Version']).copy()
        df_22 = df[df['CF_Version'] == 22].drop(columns=['CF_Version']).copy()

        return df_21, df_22

    def get_recommendations(self, identifier, df_version, top_n=10):
        # Find the target row
        mask = (df_version['name'] == identifier) | (df_version['circle_code'] == identifier)
        target_data = df_version[mask]

        if target_data.empty:
            return f"'{identifier}' not found in the provided dataset."

        # Use first match if multiple found within same DF
        target_name = target_data.iloc[0]['name']

        # Drop metadata for distance calculation
        target_features = target_data.iloc[[0]].drop(columns=['name', 'circle_code'])
        candidates = df_version[df_version['name'] != target_name].copy()
        candidate_features = candidates.drop(columns=['name', 'circle_code'])

        # Calculate distances
        distances = cdist(target_features.values, candidate_features.values, metric='jaccard').flatten()
        candidates['distance'] = distances

        return candidates[['circle_code', 'name', 'distance']].sort_values('distance').head(top_n)

def create_recommendation_subtab(df):
    if df is None:
        return pn.pane.Markdown("Data not loaded.")

    # 1. Load recommender or instantiate it
    try:
        pipeline_path = os.path.join(os.path.dirname(__file__), '..', '..', 'pipelines', 'recommender_pipeline.pkl')
        import __main__
        if not hasattr(__main__, 'CircleRecommender'):
            __main__.CircleRecommender = CircleRecommender
        
        if os.path.exists(pipeline_path):
            recommender = joblib.load(pipeline_path)
        else:
            print(f"Warning: Pipeline file not found at {pipeline_path}. Using fresh instance.")
            recommender = CircleRecommender()
    except Exception as e:
        print(f"Error loading recommender pipeline: {e}")
        recommender = CircleRecommender()

    # Preprocess the data
    df_rec_21, df_rec_22 = recommender.prepare_raw_data(df)

    # 2. UI Components
    desc_main = pn.pane.HTML("""
        <div style="padding: 10px 0; color: #2c3e50; font-size: 1.15rem; margin-bottom: 20px;">
            <p style="margin: 0;">Selamat Datang di Sistem Rekomendasi. Silakan pilih booth sirkel yang diinginkan, lalu sistem akan mencari sirkel yang mirip dengan sirkel tersebut.</p>
        </div>
    """, sizing_mode='stretch_width')

    desc_distance = pn.pane.HTML("""
        <div style="background-color: #f8f9fa; border-left: 5px solid #007bff; padding: 15px; border-radius: 4px; margin: 15px 0;">
            <p style="margin: 0; color: #495057;">
                <strong>Keterangan:</strong> Sistem rekomendasi sirkel menggunakan Jaccard Distance. Semakin nilai distance mendekati 0, maka semakin mirip satu sirkel dengan yang lain.
            </p>
        </div>
    """, sizing_mode='stretch_width')
    
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

    def create_recommendation_ui(version_name, df_rec, df_original):
        top_n_selector = pn.widgets.Select(
            name='Jumlah Rekomendasi', options=[5, 10, 20], value=5, width=150
        )
        
        # Build autocomplete options with dual entries for prefix matching
        all_entries = df_rec[['circle_code', 'name']].drop_duplicates()
        options_list = []
        code_lookup = {}
        for _, row in all_entries.iterrows():
            code = str(row['circle_code']).strip() if pd.notna(row['circle_code']) else ''
            name = str(row['name']).strip() if pd.notna(row['name']) else ''
            by_code = f"{code} ~ {name}"; options_list.append(by_code); code_lookup[by_code] = code
            by_name = f"{name} ~ {code}"; options_list.append(by_name); code_lookup[by_name] = code

        search_input = pn.widgets.AutocompleteInput(
            name=f'Cari Sirkel (Nama / Kode Sirkel) di {version_name}', 
            options=options_list, placeholder='Ketik nama atau kode sirkel...',
            min_characters=1, case_sensitive=False, restrict=False, sizing_mode='stretch_width'
        )

        btn_search = pn.widgets.Button(name='Cari Rekomendasi', button_type='success', width=180, height=45, align='end')
        
        results_pane = pn.Column(sizing_mode='stretch_width', margin=(10, 0))

        def execute_search(event=None):
            raw_val = str(search_input.value).strip()
            if not raw_val:
                results_pane.clear()
                results_pane.append(pn.pane.Alert("Silakan ketik nama/kode sirkel terlebih dahulu.", alert_type="warning"))
                return

            search_val = code_lookup.get(raw_val, raw_val)
            n = top_n_selector.value
            res = recommender.get_recommendations(search_val, df_rec, top_n=n)

            if isinstance(res, str):
                results_pane.clear()
                results_pane.append(pn.pane.Alert(f"Sirkel '{search_val}' tidak ditemukan di data {version_name}. Pastikan penulisan sesuai.", alert_type="warning"))
                return

            res['distance'] = res['distance'].round(3)

            # Get original metadata
            v_num = 22 if version_name == 'CF22' else 21
            df_v = df_original[df_original['CF_Version'] == v_num]
            
            sells_cols = [col for col in df_v.columns if col.startswith('Sells')]
            meta_cols = ['circle_code', 'name', 'day', 'rating', 'circle_type', 'fandom', 'other_fandom', 'circle_cut'] + sells_cols
            
            res_full = res.merge(df_v[meta_cols], on=['circle_code', 'name'], how='left')

            # Get target circle for display
            target_mask = (df_v['name'] == search_val) | (df_v['circle_code'] == search_val)
            target_row = df_v[target_mask].iloc[0]

            def render_circle_card(row, distance=None):
                code = row['circle_code'] if pd.notna(row['circle_code']) else '-'
                img_url = row['circle_cut'] if pd.notna(row['circle_cut']) and str(row['circle_cut']).startswith('http') else 'https://via.placeholder.com/60?text=No+Img'
                
                # Combine Fandom
                fandom_list = []
                if pd.notna(row['fandom']) and str(row['fandom']).strip(): fandom_list.append(str(row['fandom']).strip())
                if pd.notna(row['other_fandom']) and str(row['other_fandom']).strip(): fandom_list.append(str(row['other_fandom']).strip())
                fandom_str = ", ".join(fandom_list) if fandom_list else "-"

                # Extract Works Type
                works_list = []
                for col in sells_cols:
                    if row[col] == 1:
                        works_list.append(col.replace('Sells', ''))
                works_str = ", ".join(works_list) if works_list else "-"

                dist_html = ""
                if distance is not None:
                    dist_html = f"""
                    <div style="flex: 0 0 auto; background-color: #e7f1ff; color: #007bff; padding: 6px 16px; border-radius: 20px; font-weight: 800; font-size: 0.9rem; border: 1px solid #cfe2ff; white-space: nowrap; margin-left: auto;">
                        Nilai: {distance:.3f}
                    </div>
                    """

                return f"""
                <div style="display: flex; flex-direction: row; align-items: center; background-color: #ffffff; border: 1px solid #e0e0e0; border-left: 5px solid #007bff; border-radius: 8px; padding: 12px 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); gap: 20px; flex-wrap: wrap;">
                    <!-- Image Section -->
                    <div style="flex: 0 0 auto; width: 70px; height: 70px; border-radius: 6px; overflow: hidden; background-color: #f8f9fa; border: 1px solid #dee2e6; display: flex; align-items: center; justify-content: center;">
                        <img src="{img_url}" style="width: 100%; height: 100%; object-fit: cover;" onerror="this.src='https://via.placeholder.com/70?text=Error'">
                    </div>
                    
                    <div style="flex: 0 0 auto; font-weight: bold; color: #007bff; font-size: 1.2rem; min-width: 80px;">
                        {code}
                    </div>
                    <div style="flex: 1 1 180px; font-weight: 700; color: #2c3e50; font-size: 1.1rem;">
                        {row['name']}
                    </div>
                    <div style="flex: 2 1 350px; display: flex; flex-direction: column; gap: 4px; font-size: 0.9rem; color: #6c757d;">
                        <div style="display: flex; gap: 15px; flex-wrap: wrap;">
                            <div>📅 <span style="color: #343a40; font-weight: 600;">{row['day']}</span></div>
                            <div>🚦 <span style="color: #343a40; font-weight: 600;">{row['rating']}</span></div>
                            <div>🏢 <span style="color: #343a40; font-weight: 600;">{row['circle_type']}</span></div>
                        </div>
                        <div style="margin-top: 1px;">🎨 <span style="color: #495057; font-weight: 600;">Fandom:</span> <span style="color: #212529;">{fandom_str}</span></div>
                        <div>📚 <span style="color: #495057; font-weight: 600;">Works Type:</span> <span style="color: #212529;">{works_str}</span></div>
                    </div>
                    {dist_html}
                </div>
                """

            # Create full HTML with sections
            final_html = '<div style="display: flex; flex-direction: column; gap: 20px; width: 100%;">'
            
            # Section 1: Selected Circle
            final_html += '<div>'
            final_html += '<h3 style="color: #2c3e50; margin-bottom: 10px; font-size: 1.2rem;">Sirkel yang Dipilih:</h3>'
            final_html += render_circle_card(target_row)
            final_html += '</div>'

            # Section 2: Recommendations
            final_html += '<div>'
            final_html += '<h3 style="color: #2c3e50; margin-bottom: 10px; font-size: 1.2rem;">Rekomendasi Sirkel yang Mirip:</h3>'
            final_html += '<div style="display: flex; flex-direction: column; gap: 12px;">'
            for _, row in res_full.iterrows():
                final_html += render_circle_card(row, distance=row['distance'])
            final_html += '</div></div>'
            
            final_html += '</div>'
            
            results_pane.clear()
            results_pane.append(pn.pane.HTML(final_html, sizing_mode='stretch_width'))

        btn_search.on_click(execute_search)
        search_input.param.watch(lambda e: execute_search(), 'value')
        top_n_selector.param.watch(lambda e: execute_search() if search_input.value else None, 'value')

        return pn.Column(
            pn.Row(search_input, btn_search, align='end', sizing_mode="stretch_width"),
            pn.Row(top_n_selector, sizing_mode="stretch_width"),
            results_pane,
            sizing_mode="stretch_width",
            margin=(15, 0)
        )

    cf22_ui = create_recommendation_ui('CF22', df_rec_22, df)
    cf21_ui = create_recommendation_ui('CF21', df_rec_21, df)

    cf_tabs = pn.Tabs(
        ('CF22', cf22_ui),
        ('CF21', cf21_ui),
        stylesheets=[tab_stylesheet],
        margin=(10, 0)
    )

    return pn.Column(
        desc_main,
        cf_tabs,
        desc_distance,
        sizing_mode="stretch_width"
    )
