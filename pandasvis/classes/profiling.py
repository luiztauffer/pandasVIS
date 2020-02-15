from PySide2 import QtCore
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QPushButton,
                               QStyle)
from pandas_profiling import ProfileReport
import os


class PandasProfiling(QWidget):
    menu_parent = "None"
    menu_name = "Profile"

    def __init__(self, parent):
        """Description of this module."""
        super().__init__()
        self.parent = parent
        self.name = "Profile"

        self.html = QWebEngineView()

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
        self.vbox.addWidget(self.html)
        self.setLayout(self.vbox)

    def update_html(self, url):
        """Loads temporary HTML file and renders it."""
        self.html.load(url)
        self.html.show()

    def run(self):
        """Runs module."""
        # Select variables from Dataframe
        self.parent.update_selected_primary()
        df = self.parent.df[self.parent.selected_primary]
        self.parent.write_to_logger(txt="Preparing " + self.name + "... please wait.")
        self.parent.tabs_bottom.setCurrentIndex(1)
        self.thread = BusyThread(self, df)
        self.thread.finished.connect(self.thread_finished)
        self.thread.start()

    def thread_finished(self):
        error = self.thread.error
        self.thread.quit()
        if error is None:
            # Load html to object
            url = QtCore.QUrl.fromLocalFile(os.path.join(self.parent.temp_dir, self.name + '.html'))
            self.update_html(url=url)

            # Makes new tab on parent and load it with new object
            self.parent.new_tab_top(self, self.name)
            # Writes at Logger
            self.parent.write_to_logger(txt=self.name + " ready!")
        else:
            self.parent.write_to_logger(txt="ERROR:")
            self.parent.write_to_logger(txt=str(error))

    def close_threads(self):
        """Closes threads."""
        pass


class BusyThread(QtCore.QThread):
    def __init__(self, parent, df):
        super().__init__()
        self.parent = parent
        self.df = df
        self.error = None

    def run(self):
        import matplotlib
        matplotlib.use('Agg')
        try:
            # Generates
            self.profile = ProfileReport(self.df, title='Summary Report', html={'style': {'full_width': True}})
            # Saves html to temporary folder
            self.profile.to_file(os.path.join(self.parent.parent.temp_dir, self.parent.name + '.html'), silent=True)
            self.error = None
        except Exception as error:
            self.error = error
