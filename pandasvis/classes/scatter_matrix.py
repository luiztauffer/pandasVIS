from PyQt5 import QtCore
from PyQt5.QtWidgets import (QWidget, QVBoxLayout)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from pandasvis.dialogs.dialogs_filter import FilterVariablesDialog
from plotly.offline import plot as plt_plot
import plotly.graph_objs as go
from plotly import tools
from sklearn.neighbors import KernelDensity
import numpy as np
import pandas as pd
import os


class ScatterMatrix(QWidget):
    menu_parent = "Tabular"
    menu_name = "Scatter Matrix"

    def __init__(self, parent):
        """Produces a scatter matrix plot with selected variables."""
        super().__init__()
        self.parent = parent
        self.name = "Scatter Matrix"

        self.scatter_matrix = QWebEngineView()
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.scatter_matrix)
        self.setLayout(self.vbox)

    def update_html(self, url):
        """Loads temporary HTML file and render it."""
        self.scatter_matrix.load(url)
        self.scatter_matrix.show()

    @staticmethod
    def make_object(parent):
        """Makes object to be placed in new tab."""
        obj = ScatterMatrix(parent)
        # Select variables from Dataframe
        parent.update_selected_primary()
        df = parent.df[parent.selected_primary]
        # Open filter by condition dialog
        w = FilterVariablesDialog(parent, df)
        if w.value == 1:
            # Generate a dictionary of plotly plots
            sm = custom_scatter_matrix(w.df, groupby=w.group_by)
            # Saves html to temporary folder
            plt_plot(figure_or_data=sm,
                     filename=os.path.join(parent.temp_dir, 'scatter_matrix.html'),
                     auto_open=False)
            # Load scatter matrix html on object
            url = QtCore.QUrl.fromLocalFile(os.path.join(parent.temp_dir, 'scatter_matrix.html'))
            obj.update_html(url=url)
            # Makes new tab on parent and load it with new object
            parent.new_tab_top(obj, obj.name)


def custom_scatter_matrix(df, bins=10, color='grey', size=2, title_text=None,
                          hist_type='kde', kde_width=None, groupby=None,
                          palette=None, **iplot_kwargs):
    if palette is None:
        # Tableau10 scheme
        palette = ["#4e79a7", "#f28e2c", "#e15759", "#76b7b2", "#59a14f",
                   "#edc949", "#af7aa1", "#ff9da7", "#9c755f", "#bab0ab"]

    columns = df.columns.to_list()
    if groupby is not None:
        grouped = df.groupby(groupby)
        groups_names = list(grouped.groups.keys())
        columns.remove(groupby)
    else:
        groups_names = ['all']

    # Remove non-numerical columns
    for col in columns:
        dtype = str(df[col].dtypes)
        if not (dtype == 'int64' or dtype == 'float64'):
            columns.remove(col)

    nVars = len(columns)
    figs = tools.make_subplots(rows=nVars, cols=nVars, print_grid=False)

    for cgrp, grp in enumerate(groups_names):
        if grp == 'all':
            df_aux = df
        else:
            df_aux = grouped.get_group(grp)
        ii = -1
        for ci, i in enumerate(columns):
            for cj, j in enumerate(columns):
                ii += 1
                if i == j:   # univariate distribution
                    y = df_aux[i].to_numpy()
                    if hist_type == 'kde':    # Gaussian KDE
                        if kde_width is None:
                            bandwidth = 0.1*np.nanstd(y)/np.abs(np.nanmean(y))
                        Ym = np.min(df[i].to_numpy())
                        YM = np.max(df[i].to_numpy())
                        xx = np.linspace(Ym, YM, 200)
                        kde = KernelDensity(kernel='gaussian', bandwidth=bandwidth).fit(y.reshape(-1, 1))
                        log_dens = kde.score_samples(xx.reshape(-1, 1))
                        fig = go.Scatter(
                            x=xx, y=np.exp(log_dens),
                            mode='lines', fill='tozeroy',
                            line=dict(color=palette[cgrp], width=1),
                            legendgroup=grp,
                            name=grp,
                            showlegend=[True if ((ci == 0) and (cj == 0)) else False][0],
                        )
                    elif hist_type == 'hist':    # histogram
                        fig = df_aux.iplot(
                            kind='histogram', keys=[i],
                            asFigure=True, bins=bins
                        )
                elif j < i:    # bi-variate scatter plot
                    y1 = df_aux[j].to_numpy()
                    Ym1 = np.min(y1)
                    YM1 = np.max(y1)
                    y2 = df_aux[i].to_numpy()
                    Ym2 = np.min(y2)
                    YM2 = np.max(y2)
                    fig = go.Scatter(
                        x=y1, y=y2,
                        mode='markers',
                        marker=dict(
                            size=5,
                            opacity=0.9,
                            color=palette[cgrp],
                            line=dict(width=0),
                        ),
                        legendgroup=grp,
                        name=grp,
                        showlegend=False,
                        # xaxis='x'+str(ii),
                        yaxis='y'+str(ii),
                    )
                else:
                    fig = go.Scatter(x=[], y=[])
                    figs['layout']['xaxis'+str(ii+1)].update(
                        showticklabels=False,
                        zeroline=False,
                        showline=False,
                        showgrid=False)
                    figs['layout']['yaxis'+str(ii+1)].update(
                        showticklabels=False,
                        zeroline=False,
                        showline=False,
                        showgrid=False
                    )
                # Y labels
                if cj == 0:
                    figs['layout']['yaxis'+str(ii+1)].update(title=i)
                figs.append_trace(fig, ci+1, cj+1)

        # Legend
        legend_layout = go.layout.Legend(
            font=dict(size=15, color="black"),
        )
        figs.layout.update(legend=legend_layout)
        # Title
        title_layout = go.layout.Title(
            text=['Grouped by: '+groupby if groupby is not None else None][0],
            xref="paper",
            x=0,
        )
        figs.layout.update(title=title_layout)

        # figs['layout']['xaxis1'].update(anchor='x2')
        # figs['layout']['xaxis2'].update(anchor='x2')
        # figs['layout']['xaxis3'].update(anchor='x2')

    return figs
