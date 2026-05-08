import panel as pn

def create_tab(df=None):
    return pn.Column(
        pn.pane.Markdown("# Advanced Analysis\n*Clustering and Apriori will go here.*"),
        sizing_mode="stretch_width"
    )
