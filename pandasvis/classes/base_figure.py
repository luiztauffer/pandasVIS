from PySide2 import QtCore
from PySide2.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QPushButton,
                               QStyle)
from qtvoila import QtVoila
import os


class BaseFigure(QWidget):
    menu_parent = "Tabular"  # "Tabular", "Time Series"
    menu_name = "ModuleTemplate"

    def __init__(self, parent):
        """Base figure to be added as a Tab."""
        super().__init__()
        self.parent = parent
        self.name = self.menu_name

        self.voila_widget = QtVoila()

        self.bt_close = QPushButton('Close')
        self.bt_close.setIcon(self.style().standardIcon(QStyle.SP_DialogCloseButton))
        self.bt_close.clicked.connect(lambda: self.parent.close_tab_top(self))

        self.bt_maxfig = QPushButton('Expand / Retract')
        self.bt_maxfig.setIcon(self.style().standardIcon(QStyle.SP_TitleBarMaxButton))
        self.bt_maxfig.clicked.connect(self.parent.toggle_max_figure)

        self.grid1 = QGridLayout()
        self.grid1.setColumnStretch(0, 1)
        self.grid1.addWidget(QWidget(), 0, 0, 1, 3)
        self.grid1.addWidget(self.bt_maxfig, 0, 4, 1, 1)
        self.grid1.addWidget(self.bt_close, 0, 5, 1, 1)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.grid1)
        self.vbox.addWidget(self.voila_widget)
        self.setLayout(self.vbox)

    def make_figure(self, **kwargs):
        """Custom code to produce figure to be placed in GUI."""
        fig = []
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
        kwargs = {'df': df}
        return kwargs

    def run(self):
        """Runs module."""
        # run custom defined preprocessing
        args, kwargs = self.pre_run()
        args.insert(0, self)
        # Update GUI logger
        self.parent.write_to_logger(txt="Preparing " + self.name + "... please wait.")
        self.parent.tabs_bottom.setCurrentIndex(1)
        # Starts figure making Thread
        self.fig_thread = makefigureThread(*args, **kwargs)
        self.fig_thread.finished.connect(self.fig_thread_finished)
        self.fig_thread.start()

    def fig_thread_finished(self):
        error = self.fig_thread.error
        self.fig_thread.quit()
        if error is None:
            # Write Figure + ipywidgets to a .ipynb file
            code = """
                import plotly
                import os
                from pandasvis.other.fig_controls import DashBoard

                fpath = os.path.join(r'""" + self.parent.temp_dir + """', '""" + self.name + '.json' + """')
                fig = plotly.io.read_json(fpath)
                fig_widget = plotly.graph_objs.FigureWidget(fig)
                dashboard = DashBoard(fig_widget)
                dashboard"""
            # Stores code on voila widget
            self.voila_widget.code = code
            # Runs Voila process and renders result on widget
            self.voila_widget.run_voila()

            # Load Voila instance on GUI
            self.parent.new_tab_top(self, self.name)
            self.parent.write_to_logger(txt=self.name + " ready!")
        else:
            self.parent.write_to_logger(txt="ERROR:")
            self.parent.write_to_logger(txt=str(error))

    def close_threads(self):
        """Closes threads."""
        self.voila_widget.close_renderer()


class makefigureThread(QtCore.QThread):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.parent = args[0]
        self.figure_function_args = args[1:]
        self.figure_function_kwargs = kwargs
        self.error = None

    def run(self):
        try:
            self.parent.figure = self.parent.make_figure(
                *self.figure_function_args,
                **self.figure_function_kwargs
            )
            # Saves json to temporary folder
            save_file_path = os.path.join(self.parent.parent.temp_dir, self.parent.name + '.json')
            self.parent.figure.write_json(save_file_path)
            self.error = None
        except Exception as error:
            self.error = error
