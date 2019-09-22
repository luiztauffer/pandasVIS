from PyQt5 import QtCore
from PyQt5.QtWidgets import (QWidget, QVBoxLayout)
from PyQt5.QtWebEngineWidgets import QWebEngineView
import os


class ModuleTemplate(QWidget):
    menu_parent = "Tabular"  # "Tabular", "Time Series"
    menu_name = "Module Template"

    def __init__(self, parent):
        """Description of this module."""
        super().__init__()
        self.parent = parent
        self.name = "Module name"

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
        obj = ModuleTemplate(parent)
        # Select variables from Dataframe
        parent.update_selected_primary()
        df = parent.df[parent.selected_primary]
        # Runs the module
        my_module_processing(df=df)
        # Load html to object
        url = QtCore.QUrl.fromLocalFile(os.path.join(parent.temp_dir, 'just_created.html'))
        obj.update_html(url=url)
        # Makes new tab on parent and load it with new object
        parent.new_tab_top(obj, obj.name)


def my_module_processing(df):
    """
    This is the new module, it will get the Dataframe and do cool stuff with it.
    For example, it can produce an interactive figure and save it to html to be
    loaded later by a tab in PandasVIS.
    """
    return df
