import panel as pn
import pandas as pd
import os

# Import subtabs
from .subtabs.subtab04_recommendation import create_recommendation_subtab
from .subtabs.subtab04_rating import create_rating_subtab

def create_tab(df=None):
    if df is None:
        return pn.pane.Markdown("Data not loaded.")

    # Tab Styling (Consistent with tab02)
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

    # Initialize subtabs
    recommendation_subtab = create_recommendation_subtab(df)
    rating_subtab = create_rating_subtab(df)
    
    # Main Tabs container
    main_tabs = pn.Tabs(
        ("Recommendation", recommendation_subtab),
        ("Faktor Berpengaruh", rating_subtab),
        stylesheets=[tab_stylesheet],
        margin=(20, 0)
    )

    # Return with styling consistent with tab03_ed_analysis.py
    return pn.Column(
        pn.pane.HTML("<h2 style='color: #2c3e50; border-bottom: 2px solid #007bff; padding-bottom: 10px; margin-bottom: 20px;'>Advanced Analysis</h2>"),
        main_tabs,
        sizing_mode="stretch_width",
        margin=(20, 20)
    )
