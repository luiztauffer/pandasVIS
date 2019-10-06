from PyQt5 import QtCore
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QPushButton,
                             QStyle)
import os
import nbformat as nbf


class BaseFigure(QWidget):
    menu_parent = "Tabular"  # "Tabular", "Time Series"
    menu_name = "ModuleTemplate"

    def __init__(self, parent):
        """Description of this module."""
        super().__init__()
        self.parent = parent
        self.name = self.menu_name

        self.html = QWebEngineView()

        self.bt_close = QPushButton('Close')
        self.bt_close.setIcon(self.style().standardIcon(QStyle.SP_DialogCloseButton))
        self.bt_close.clicked.connect(lambda: self.parent.close_tab_top(self))

        self.bt_maxfig = QPushButton('Expand / Retract')
        self.bt_maxfig.setIcon(self.style().standardIcon(QStyle.SP_TitleBarMaxButton))
        self.bt_maxfig.clicked.connect(self.parent.toggle_max_figure)

        self.bt_layout = QPushButton('Layout')
        self.bt_layout.setIcon(self.style().standardIcon(QStyle.SP_FileDialogListView))
        self.bt_layout.clicked.connect(self.layout_dialog)

        self.grid1 = QGridLayout()
        self.grid1.setColumnStretch(0, 1)
        self.grid1.addWidget(QWidget(), 0, 0, 1, 3)
        self.grid1.addWidget(self.bt_layout, 0, 3, 1, 1)
        self.grid1.addWidget(self.bt_maxfig, 0, 4, 1, 1)
        self.grid1.addWidget(self.bt_close, 0, 5, 1, 1)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.grid1)
        self.vbox.addWidget(self.html)
        self.setLayout(self.vbox)

    def layout_dialog(self):
        """Opens layout dialog"""
        w = LayoutDialog(parent=self)

    def layout_update(self, changes):
        """Updates figure layout with dictionary in changes"""
        self.figure['layout'].update(changes)
        nSubs = sum(['xaxis' in i for i in self.figure['layout']])
        for i in range(nSubs):
            xname = 'xaxis' if i == 0 else 'xaxis'+str(i)
            yname = 'yaxis' if i == 0 else 'yaxis'+str(i)
            self.figure['layout'][xname].update(changes['xaxis'])
            self.figure['layout'][yname].update(changes['yaxis'])
        # Saves html to temporary folder
        plt_plot(figure_or_data=self.figure,
                 filename=os.path.join(self.parent.temp_dir, self.name+'.html'),
                 auto_open=False)
        url = QtCore.QUrl.fromLocalFile(os.path.join(self.parent.temp_dir, self.name+'.html'))
        self.update_html(url=url)

    def update_html(self, url):
        """Loads temporary HTML file and render it."""
        self.html.load(QtCore.QUrl(url))
        self.html.show()

    def figthread_finished(self):
        error = self.figthread.error
        if error is None:
            # Layout editing - Slow method -------------------------------------
            # url = QtCore.QUrl.fromLocalFile(os.path.join(self.parent.temp_dir,
            #                                              self.name+'.html'))
            # self.update_html(url=url)
            # ------------------------------------------------------------------

            # Write Figure + ipywidgets to a .ipynb file
            nb = nbf.v4.new_notebook()
            code = """
                import plotly
                import os
                from pandasvis.other.fig_controls import DashBoard

                fpath = os.path.join(r'""" + self.parent.temp_dir + """', '""" + self.name+'.json' + """')
                fig = plotly.io.read_json(fpath)
                fig_widget = plotly.graph_objs.FigureWidget(fig)
                dashboard = DashBoard(fig_widget)
                dashboard"""
            nb['cells'] = [nbf.v4.new_code_cell(code)]
            nbf.write(nb, self.name+'.ipynb')
            # Run instance of Voila with the just saved .ipynb file
            self.voilathread = voilaThread(parent=self, port=7000)
            self.voilathread.start()
            # Load Voila instance on GUI
            self.update_html('http://localhost:7000/')
            self.parent.new_tab_top(self, self.name)
            self.parent.write_to_logger(txt=self.name + " ready!")
        else:
            self.parent.write_to_logger(txt="ERROR:")
            self.parent.write_to_logger(txt=str(error))

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
        self.figthread = makefigureThread(*args, **kwargs)
        self.figthread.finished.connect(self.figthread_finished)
        self.figthread.start()


class voilaThread(QtCore.QThread):
    def __init__(self, parent, port):
        super().__init__()
        self.parent = parent
        self.port = port

    def run(self):
        os.system("voila "+self.parent.name+'.ipynb --no-browser --port '+str(self.port))

    def stop(self):
    #    import signal
    #    os.system(signal.SIGINT)
        pass


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
            save_file_path = os.path.join(self.parent.parent.temp_dir, self.parent.name+'.json')
            self.parent.figure.write_json(save_file_path)

            # Saves html to temporary folder
            # save_file_path = os.path.join(self.parent.parent.temp_dir, self.parent.name+'.html')
            # plt_plot(figure_or_data=self.parent.figure,
            #          filename=save_file_path,
            #          auto_open=False)
            self.error = None
        except Exception as error:
            self.error = error
