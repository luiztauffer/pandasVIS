from pandasvis.classes.base_figure import BaseFigure
from pandasvis.dialogs.filter_variables import FilterVariablesDialog
from pandasvis.utils.styles import palettes
from pandasvis.utils.layouts import lay_base

import plotly
import plotly.graph_objs as go
from sklearn.neighbors import KernelDensity
import numpy as np


class ScatterMatrix(BaseFigure):
    menu_parent = "Tabular"
    menu_name = "ScatterMatrix"

    def __init__(self, parent):
        """Module to create Joyplots."""
        super().__init__(parent)

    def make_figure(self, *args, **kwargs):
        """Custom code to produce figure to be placed in GUI."""
        fig = scatter_matrix(*args, **kwargs)
        return fig

    def pre_run(self):
        """
        Custom code to preprocess dataframes and generate the keyword arguments
        needed in self.make_figure. It can contain any process you want, dialogs
        for user interface, etc...
        """
        # Select variables from Dataframe
        self.parent.update_selected_primary()
        df = self.parent.df[self.parent.selected_primary]
        # Open filter by condition dialog
        w = FilterVariablesDialog(parent=self, df=df)
        if w.value == 1:
            args = [df]
            kwargs = {'group_by': w.group_by}
            return args, kwargs


def scatter_matrix(df, bins=10, color='grey', size=2, title_text=None,
                   hist_type='kde', kde_width=None, group_by=None,
                   palette=None, **iplot_kwargs):
    # Color palette
    if palette is None:
        palette = palettes['Tableau10']

    columns = df.columns.to_list()
    if group_by is not None:
        grouped = df.groupby(group_by)
        groups_names = list(grouped.groups.keys())
        columns.remove(group_by)
    else:
        groups_names = ['all']

    # Remove non-numerical columns
    to_remove = []
    for col in columns:
        dtype = str(df[col].dtypes)
        if not (dtype == 'int64' or dtype == 'float64'):
            to_remove.append(col)
    for col in to_remove:
        columns.remove(col)

    nVars = len(columns)
    figs = plotly.subplots.make_subplots(rows=nVars, cols=nVars, print_grid=False)
    figs['layout'].update(lay_base)

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
                    figs.add_trace(fig, row=ci+1, col=cj+1)
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
                    figs.add_trace(fig, row=ci+1, col=cj+1)
                # Y labels
                if cj == 0:
                    figs['layout']['yaxis'+str(ii+1)].update({"title": {'text': i}})

        # Legend
        legend_layout = go.layout.Legend(
            font=dict(size=15, color="black"),
        )
        figs['layout'].update(legend=legend_layout)
        # Title
        title_text=['Grouped by: '+group_by if group_by is not None else None][0]
        figs.layout.update({"title": {'text': title_text}})

    return figs
