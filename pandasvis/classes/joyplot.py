from pandasvis.classes.base_figure import BaseFigure
from pandasvis.dialogs.joyplot_filter import JoyplotFilterDialog
from pandasvis.utils.functions import AutoDictionary
from pandasvis.utils.styles import palettes
from pandasvis.utils.layouts import lay_base

import plotly
import plotly.graph_objs as go
from sklearn.neighbors import KernelDensity
import numpy as np


class Joyplot(BaseFigure):
    menu_parent = "Tabular"
    menu_name = "Joyplot"

    def __init__(self, parent):
        """Module to create Joyplots."""
        super().__init__(parent)

    def make_figure(self, *args, **kwargs):
        """Custom code to produce figure to be placed in GUI."""
        fig = make_joyplot(*args, **kwargs)
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
        w = JoyplotFilterDialog(parent=self, df=df)
        if w.value == 1:
            args = [df, w.y_groups]
            kwargs = {'group_by': w.group_by}
            return args, kwargs


def make_joyplot(df, y_groups, group_by=None, hist_type='kde', kde_width=None,
                 palette=None):
    """
    Makes a Joyplot / Ridge plot.
    """

    # List of colors for multiple groups, if group_by!=None
    if palette is None:
        palette = palettes['palette_0']

    columns = df.columns.to_list()
    columns.remove(y_groups)
    # Remove non-numerical columns
    to_remove = []
    for col in columns:
        dtype = str(df[col].dtypes)
        if not (dtype == 'int64' or dtype == 'float64'):
            to_remove.append(col)
    for col in to_remove:
        columns.remove(col)

    nVars = len(columns)
    if nVars > 1:
        figs = plotly.subplots.make_subplots(rows=int(np.ceil(nVars / 2.)), cols=2, print_grid=False)
    else:
        figs = plotly.subplots.make_subplots(rows=1, cols=1, print_grid=False)
    figs['layout'].update(lay_base)

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
            bandwidth = 0.1 * np.nanstd(df[x_var]) / np.abs(np.nanmean(df[x_var]))

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
            yy_base = -ii * np.ones(len(xx)) * y_peaks[x_var]
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
                    "fillcolor": palette[jj],
                    "legendgroup": grp_2,
                    "showlegend": [True if (kk == 0) and (ii == 0) and (len(groups_names_2) > 1)
                                   else False][0],
                }
                figs.add_trace(go.Scatter(trace_base), row=(kk // 2 + 1), col=(kk % 2 + 1))
                figs.add_trace(go.Scatter(trace_pdf), row=(kk // 2 + 1), col=(kk % 2 + 1))

        xname = 'xaxis' if kk == 0 else 'xaxis' + str(kk + 1)
        yname = 'yaxis' if kk == 0 else 'yaxis' + str(kk + 1)
        figs['layout'][xname].update({
            "title": {'text': x_var, 'font': {"family": "Balto"}},
            "type": "linear",
            "range": [xx_min, xx_max],
            "showgrid": True,
            "showline": False,
            "zeroline": False
        })
        figs['layout'][yname].update({
            "title": {'font': {"family": "Balto"}},
            "type": "linear",
            "ticktext": groups_names,
            "tickvals": [-i * y_peaks[x_var] for i in range(len(groups_names))],
            "zeroline": False,
            "showline": False,
            "showgrid": True,
            "gridcolor": "#ffffff",
            "gridwidth": 1
        })

    return figs
