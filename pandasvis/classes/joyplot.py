from PyQt5 import QtCore
from PyQt5.QtWidgets import (QWidget, QVBoxLayout)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from pandasvis.dialogs.joyplot_filter import JoyplotFilterDialog
from plotly.offline import plot as plt_plot
import plotly.graph_objs as go
from plotly import tools
from sklearn.neighbors import KernelDensity
import numpy as np
import pandas as pd
import os


class Joyplot(QWidget):
    menu_parent = "Tabular"
    menu_name = "Joyplot"

    def __init__(self, parent):
        """Description of this module."""
        super().__init__()
        self.parent = parent
        self.name = "Joyplot"

        self.module = QWebEngineView()
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.module)
        self.setLayout(self.vbox)

    def update_html(self, url):
        """Loads temporary HTML file and render it."""
        self.module.load(url)
        self.module.show()

    @staticmethod
    def make_object(parent):
        """Makes object to be placed in new tab."""
        obj = Joyplot(parent)
        # Select variables from Dataframe
        parent.update_selected_primary()
        df = parent.df[parent.selected_primary]
        # Open filter by condition dialog
        w = JoyplotFilterDialog(parent=parent, df=df)
        if w.value == 1:
            # Generate a dictionary of plotly plots
            jp, layout = make_joyplot(df=w.df,
                                      y_groups=w.y_groups,
                                      group_by=w.group_by)

            parent.console.push_vars({'jp': jp})
            parent.console.push_vars({'lay': layout})

            # Saves html to temporary folder
            plt_plot(figure_or_data=jp,
                     filename=os.path.join(parent.temp_dir, obj.name+'.html'),
                     auto_open=False)
        # Load html to object
        url = QtCore.QUrl.fromLocalFile(os.path.join(parent.temp_dir, obj.name+'.html'))
        obj.update_html(url=url)
        # Makes new tab on parent and load it with new object
        parent.new_tab_top(obj, obj.name)


def make_joyplot(df, y_groups, group_by=None, hist_type='kde', kde_width=None):
    """
    Makes a Joyplot / Ridge plot.
    """
    columns = df.columns.to_list()
    columns.remove(y_groups)
    # Remove non-numerical columns
    for col in columns:
        dtype = str(df[col].dtypes)
        if not (dtype == 'int64' or dtype == 'float64'):
            columns.remove(col)
    nVars = len(columns)
    figs = tools.make_subplots(rows=int(np.ceil(nVars/2.)), cols=2, print_grid=False)

    layout = {}
    for kk, x_var in enumerate(columns):
        xx_min = df[x_var].min()
        xx_max = df[x_var].max()
        xx = np.linspace(xx_min, xx_max, 100)
        if kde_width is None:
            bandwidth = 0.1*np.nanstd(df[x_var])/np.abs(np.nanmean(df[x_var]))
        grouped = df.groupby(y_groups)
        groups_names = list(grouped.groups.keys())

        for ii, grp in enumerate(groups_names):
            df_aux = grouped.get_group(grp)
            y = df_aux[x_var].to_numpy()
            kde = KernelDensity(kernel='gaussian', bandwidth=bandwidth).fit(y.reshape(-1, 1))
            log_dens = kde.score_samples(xx.reshape(-1, 1))
            yy = np.exp(log_dens)
            yy_base = ii*np.ones(len(xx))
            trace_base = {
              "line": {
                "color": "#000000",
                "width": 0.1
              },
              "mode": "lines",
              "type": "scatter",
              "x": xx.tolist(),
              "y": yy_base.tolist(),
              "showlegend": False,
            }
            trace_pdf = {
              "fill": "tonexty",
              "line": {
                "color": "#000000",
                "shape": "spline",
                "width": 0.5
              },
              "mode": "lines",
              "name": grp,
              "type": "scatter",
              "x": xx.tolist(),
              "y": (yy_base + yy).tolist(),
              "fillcolor": "rgba(134, 149, 184, 0.8)",
              "legendgroup": grp,
              "showlegend": [True if kk == 0 else False][0],
            }
            figs.add_trace(go.Scatter(trace_base), row=(kk//2+1), col=(kk % 2+1))
            figs.add_trace(go.Scatter(trace_pdf), row=(kk//2+1), col=(kk % 2+1))

        if kk == 0:
            li = ''
        else:
            li = str(kk+1)

        figs['layout']["xaxis"+li].update({
            "type": "linear",
            #"dtick": 5,
            "range": [xx_min, xx_max],
            "title": x_var,
            "ticklen": 4,
            "showgrid": False,
            "showline": False,
            "zeroline": True
        })
        figs['layout']["yaxis"+li].update({
            "type": "linear",
            "ticklen": 4,
            "showgrid": True,
            "showline": False,
            "ticktext": groups_names,
            "tickvals": [0, 1, 2],
            "zeroline": False,
            "gridcolor": "rgb(255,255,255)",
            "gridwidth": 1
        })
    figs['layout'].update({
        "font": {"family": "Balto"},
        "title": "A cool Joyplot/Ridgelines",
        "hovermode": "closest",
        "plot_bgcolor": "rgb(255,255,255)"
    })

    return figs, layout
