from PyQt5 import QtCore
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QPushButton,
                             QStyle)
from PyQt5.QtWebEngineWidgets import QWebEngineView

import numpy as np
import pandas as pd
import pandas_profiling
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

        self.grid1 = QGridLayout()
        self.grid1.setColumnStretch(0, 1)
        self.grid1.addWidget(QWidget(), 0, 0, 1, 5)
        self.grid1.addWidget(self.bt_close, 0, 5, 1, 1)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.grid1)
        self.vbox.addWidget(self.html)
        self.setLayout(self.vbox)

    def update_html(self, url):
        """Loads temporary HTML file and render it."""
        self.html.load(url)
        self.html.show()

    def make_plot(self):
        """Makes object to be placed in new tab."""
        def finish_thread(obj, error):
            if error is None:
                # Load html to object
                url = QtCore.QUrl.fromLocalFile(os.path.join(obj.parent.temp_dir, obj.name+'.html'))
                obj.update_html(url=url)
                # Makes new tab on parent and load it with new object
                obj.parent.new_tab_top(obj, obj.name)
                # Writes at Logger
                obj.parent.write_to_logger(txt=self.name + " ready!")
            else:
                obj.parent.write_to_logger(txt="ERROR:")
                obj.parent.write_to_logger(txt=str(error))

        # Select variables from Dataframe
        self.parent.update_selected_primary()
        df = self.parent.df[self.parent.selected_primary]
        self.parent.write_to_logger(txt="Preparing " + self.name + "... please wait.")
        self.parent.tabs_bottom.setCurrentIndex(1)
        thread = BusyThread(df, self)
        thread.finished.connect(lambda: finish_thread(self, error=thread.error))
        thread.start()


# Runs conversion function, useful to wait for thread
class BusyThread(QtCore.QThread):
    def __init__(self, df, obj):
        super().__init__()
        self.df = df
        self.obj = obj
        self.error = None

    def run(self):
        try:
            # Generates
            self.df_profile = self.df.profile_report(title='Summary Report', style={'full_width': True})
            # Saves html to temporary folder
            self.df_profile.to_file(os.path.join(self.obj.parent.temp_dir, self.obj.name+'.html'), silent=True)
            self.error = None
        except Exception as error:
            self.error = error
