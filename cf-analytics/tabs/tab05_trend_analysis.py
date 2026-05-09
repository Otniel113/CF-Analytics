import panel as pn
import plotly.express as px
import pandas as pd

# Import subtabs
from .subtabs.subtab05_returning_circle import create_returning_circle_subtab
from .subtabs.subtab05_fandom import create_fandom_trend_subtab

def create_tab(df=None, df_returning=None):
    if df is None:
        return pn.pane.Markdown("# Trend Analysis Area\n*Data not loaded.*", sizing_mode="stretch_width")

    # ==========================================
    # SUB-TABS (MODULARIZED)
    # ==========================================
    fandom_layout = create_fandom_trend_subtab(df)
    returning_layout = create_returning_circle_subtab(df, df_returning)

    # ==========================================
    # ASSEMBLE TABS
    # ==========================================
    subtabs_stylesheet = """
    .bk-tabs-header {
        background-color: transparent !important;
        padding-top: 5px !important;
        border-bottom: 2px solid #e9ecef !important;
    }
    .bk-tab {
        font-size: 1.1rem !important;
        padding: 10px 20px !important;
        font-weight: 500 !important;
        color: #6c757d !important;
    }
    .bk-tab.bk-active {
        color: #007bff !important;
        border-bottom: 3px solid #007bff !important;
        font-weight: 600 !important;
    }
    """
    
    trend_tabs = pn.Tabs(
        ('Fandom Trend', fandom_layout),
        ('Returning Circle', returning_layout),
        stylesheets=[subtabs_stylesheet],
        dynamic=True,
        sizing_mode="stretch_width"
    )

    layout = pn.Column(
        pn.pane.HTML("<h2 style='color: #2c3e50; border-bottom: 2px solid #007bff; padding-bottom: 10px; margin-bottom: 20px;'>Trend Analysis</h2>"),
        trend_tabs,
        sizing_mode="stretch_width",
        margin=(20, 20)
    )
    
    return layout
