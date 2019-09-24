from PyQt5 import QtCore
from PyQt5.QtWidgets import (QWidget, QVBoxLayout)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from pandasvis.dialogs.joyplot_filter import JoyplotFilterDialog
from pandasvis.utils.functions import AutoDictionary
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
            jp = make_joyplot(df=w.df,
                              y_groups=w.y_groups,
                              group_by=w.group_by)
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

    # List of colors for multiple groups, if group_by!=None
    clist = ["rgba(134, 149, 184, 0.5)", "rgba(184, 179, 134, 0.5)",
             "rgba(184, 134, 134, 0.5)", "rgba(134, 184, 132, 0.5)",
             "rgba(140, 134, 184, 0.5)", "rgba(184, 134, 176, 0.5)"]

    columns = df.columns.to_list()
    columns.remove(y_groups)
    # Remove non-numerical columns
    for col in columns:
        dtype = str(df[col].dtypes)
        if not (dtype == 'int64' or dtype == 'float64'):
            columns.remove(col)
    nVars = len(columns)
    if nVars > 1:
        figs = tools.make_subplots(rows=int(np.ceil(nVars/2.)), cols=2, print_grid=False)
    else:
        figs = tools.make_subplots(rows=1, cols=1, print_grid=False)

    # Iterations to generate curves and estimate best separation distances
    yy = AutoDictionary()
    y_peaks = AutoDictionary()
    grouped = df.groupby(y_groups)
    groups_names = list(grouped.groups.keys())
    for kk, x_var in enumerate(columns):
        xx_min = df[x_var].min()
        xx_max = df[x_var].max()
        xx = np.linspace(xx_min, xx_max, 100)
        y_peaks_aux = np.array([0])
        if kde_width is None:
            bandwidth = 0.1*np.nanstd(df[x_var])/np.abs(np.nanmean(df[x_var]))

        for ii, grp in enumerate(groups_names):
            df_aux = grouped.get_group(grp)
            if group_by is not None:
                grouped_2 = df_aux.groupby(group_by)
                groups_names_2 = list(grouped_2.groups.keys())
            else:
                groups_names_2 = ['NA']

            for jj, grp_2 in enumerate(groups_names_2):
                if len(groups_names_2) == 1:
                    df_aux_2 = df_aux
                    grp_2 = grp
                    yy_key_2 = 'NA'
                else:
                    df_aux_2 = grouped_2.get_group(grp_2)
                    yy_key_2 = grp_2
                y = df_aux_2[x_var].to_numpy()
                kde = KernelDensity(kernel='gaussian', bandwidth=bandwidth).fit(y.reshape(-1, 1))
                log_dens = kde.score_samples(xx.reshape(-1, 1))
                yy[x_var][grp][yy_key_2] = np.exp(log_dens)
                y_peaks_aux = np.append(y_peaks_aux, yy[x_var][grp][yy_key_2].max())
        y_peaks_mean = np.mean(y_peaks_aux)
        y_peaks_std = np.std(y_peaks_aux)
        y_peaks[x_var] = y_peaks_mean + y_peaks_std

    # Iterations to populate figure with plots
    for kk, x_var in enumerate(columns):
        xx_min = df[x_var].min()
        xx_max = df[x_var].max()
        xx = np.linspace(xx_min, xx_max, 100)
        for ii, grp in enumerate(groups_names):
            yy_base = -ii*np.ones(len(xx))*y_peaks[x_var]
            for jj, grp_2 in enumerate(groups_names_2):
                if len(groups_names_2) == 1:
                    yy_key_2 = 'NA'
                else:
                    yy_key_2 = grp_2
                yy_line = yy[x_var][grp][yy_key_2]
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
                  "name": grp_2,
                  "type": "scatter",
                  "x": xx.tolist(),
                  "y": (yy_base + yy_line).tolist(),
                  "fillcolor": clist[jj],
                  "legendgroup": grp_2,
                  "showlegend": [True if (kk == 0) and (ii == 0) and (len(groups_names_2) > 1)
                                 else False][0],
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
            "showgrid": True,
            "showline": False,
            "zeroline": False
        })
        figs['layout']["yaxis"+li].update({
            "type": "linear",
            "showgrid": True,
            "showline": False,
            "ticktext": groups_names,
            "tickvals": [-i*y_peaks[x_var] for i in range(len(groups_names))],
            "zeroline": False,
            "gridcolor": "rgb(255,255,255)",
            "gridwidth": 1
        })
    figs['layout'].update({
        "font": {"family": "Balto"},
        "hovermode": "closest",
        "plot_bgcolor": "rgb(255,255,255)"
    })

    return figs
