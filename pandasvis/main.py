from PySide2 import QtCore
from PySide2.QtCore import Qt
from PySide2.QtWidgets import (QWidget, QApplication, QTreeWidgetItem, QLabel,
                               QMainWindow, QFileDialog, QAction, QVBoxLayout,
                               QGridLayout, QPushButton, QTreeWidgetItemIterator,
                               QTabWidget, QSplitter, QTextEdit, QMessageBox,
                               QHBoxLayout)
from pandasvis.classes.trees import QTreeCustomPrimary, QTreeCustomSecondary
from pandasvis.classes.console_widget import ConsoleWidget
from pandasvis.utils.load_all_modules import load_all_modules
from pandasvis.classes.trees import move_to_secondary, move_to_primary
import numpy as np
import pandas as pd
import datetime
import os
import sys
import shutil


class Application(QMainWindow):
    def __init__(self, filename):
        super().__init__()

        self.resize(1200, 900)
        self.setWindowTitle('PandasVIS')

        # Initialize GUI elements
        self.init_gui()
        self.max_fig = False

        # Opens file (if argument was passed)
        if filename is not None:
            self.open_file()

        # Creates temp folder for temporary files
        self.temp_dir = os.path.join(os.getcwd(), 'temp')
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir, exist_ok=True)

        self.init_console()
        self.console.push_vars({'self': self})
        self.load_modules()
        self.show()

    def init_gui(self):
        """Initiates GUI elements."""
        mainMenu = self.menuBar()
        # File menu
        fileMenu = mainMenu.addMenu('File')
        # Adding actions to file menu
        action_open_file = QAction('Open File', self)
        fileMenu.addAction(action_open_file)
        action_open_file.triggered.connect(lambda: self.open_file(None))

        self.toolsMenu = mainMenu.addMenu('Tools')
        self.tabularMenu = self.toolsMenu.addMenu('Tabular')
        self.timeseriesMenu = self.toolsMenu.addMenu('Time Series')

        helpMenu = mainMenu.addMenu('Help')
        action_about = QAction('About', self)
        helpMenu.addAction(action_about)
        action_about.triggered.connect(self.about)

        # Left panels ----------------------------------------------------------
        self.bt_markall = QPushButton('Mark all')
        self.bt_markall.clicked.connect(self.mark_all)
        self.bt_unmarkall = QPushButton('Unmark all')
        self.bt_unmarkall.clicked.connect(self.unmark_all)
        self.bt_test = QPushButton(' ')
        self.bt_test.clicked.connect(self.test)

        self.tree_primary = QTreeCustomPrimary(parent=self)
        self.tree_primary.setAlternatingRowColors(True)
        self.tree_primary.setHeaderLabels(['Primary Variables', 'type'])
        self.tree_primary.setToolTip("Columns of the Dataframe. Can be accessed\n"
                                     "in the console with the variable 'df'")
        self.tree_primary.itemClicked.connect(self.update_selected_primary)

        self.bt_toprimary = QPushButton('To primary')
        self.bt_toprimary.clicked.connect(self.to_primary)
        self.bt_tosecondary = QPushButton('To secondary')
        self.bt_tosecondary.clicked.connect(self.to_secondary)
        self.hbox_l1 = QHBoxLayout()
        self.hbox_l1.addWidget(self.bt_toprimary)
        self.hbox_l1.addWidget(self.bt_tosecondary)

        self.tree_secondary = QTreeCustomSecondary(parent=self)
        self.tree_secondary.setAlternatingRowColors(True)
        self.tree_secondary.setHeaderLabels(['Secondary Variables', 'type'])
        self.tree_secondary.setToolTip("Secondary variables, can be added to the Dataframe.\n"
                                       "Can be accessed in the console with the variable \n"
                                       "'secondary_vars'")
        self.tree_secondary.itemClicked.connect(self.update_selected_secondary)

        self.df = pd.DataFrame(np.random.rand(100, 5), columns=['a', 'b', 'c', 'd', 'e'])
        names = ['aa', 'bb', 'cc']
        nm = [names[ind % 3] for ind in np.arange(100)]
        self.df['name'] = nm
        names_2 = ['abcd', 'ab789', 'another_class', 'yet_another', 'dfg65']
        nm_2 = [names_2[ind % 5] for ind in np.arange(100)]
        self.df['name_2'] = nm_2
        self.primary_names = list(self.df.keys())
        self.secondary_vars = {'var 3': np.zeros(100), 'var 4': np.zeros(100)}
        self.secondary_names = list(self.secondary_vars.keys())
        self.init_trees()

        self.vbox1 = QVBoxLayout()
        self.vbox1.addLayout(self.hbox_l1)
        self.vbox1.addWidget(self.tree_secondary)
        self.wbox1 = QWidget()
        self.wbox1.setLayout(self.vbox1)
        self.vsplit1 = QSplitter(Qt.Vertical)
        self.vsplit1.addWidget(self.tree_primary)
        self.vsplit1.addWidget(self.wbox1)

        self.grid_left1 = QGridLayout()
        self.grid_left1.setColumnStretch(5, 1)
        self.grid_left1.addWidget(self.bt_markall, 0, 0, 1, 2)
        self.grid_left1.addWidget(self.bt_unmarkall, 0, 2, 1, 2)
        self.grid_left1.addWidget(self.bt_test, 0, 4, 1, 1)
        self.grid_left1.addWidget(self.vsplit1, 1, 0, 1, 6)
        self.left_widget = QWidget()
        self.left_widget.setLayout(self.grid_left1)

        # Center panels -------------------------------------------------------
        # Top tabs
        self.tabs_top = QTabWidget()
        self.tab0 = QWidget()
        self.tabs_top.addTab(self.tab0, "Tools")

        # Bottom tabs
        self.tabs_bottom = QTabWidget()
        self.console = ConsoleWidget(par=self)
        self.console.setToolTip(
            "df --> Dataframe with Primary variables\n"
            "secondary_vars --> Dictionary with Secondary variables")
        self.logger = QTextEdit()
        self.logger.setReadOnly(True)
        self.tabs_bottom.addTab(self.console, "Console")
        self.tabs_bottom.addTab(self.logger, "Logger")

        self.righ_widget = QSplitter(Qt.Vertical)
        self.righ_widget.addWidget(self.tabs_top)
        self.righ_widget.addWidget(self.tabs_bottom)

        # Window layout --------------------------------------------------------
        self.hbox = QSplitter(Qt.Horizontal)
        self.hbox.addWidget(self.left_widget)     # add left panel
        self.hbox.addWidget(self.righ_widget)     # add centre panel
        self.setCentralWidget(self.hbox)

    def test(self):
        pass

    def load_modules(self):
        # Main tools tab buttons layout
        self.tools_grid = QGridLayout()
        self.tools_grid.setColumnStretch(3, 1)
        self.lbl_tabular = QLabel("Tabular")
        self.tools_grid.addWidget(self.lbl_tabular, 0, 0, 1, 2)
        # modules and lambdas lists
        self.instances_list = []
        self.modules_list = load_all_modules()
        self.lambdas_list = [(lambda a: lambda: self.instantiate_module(a))(o) for o in self.modules_list]
        for i, module in enumerate(self.modules_list):
            # Populates Menu bar
            action = QAction(module.menu_name, self)
            action.triggered.connect(self.lambdas_list[i])
            if module.menu_parent == 'None':
                self.toolsMenu.addAction(action)
            if module.menu_parent == 'Tabular':
                self.tabularMenu.addAction(action)
            elif module.menu_parent == 'Time Series':
                self.timeseriesMenu.addAction(action)
            # Populates buttons tab
            btn = QPushButton(module.menu_name)
            btn.clicked.connect(self.lambdas_list[i])
            self.tools_grid.addWidget(btn, 1, i, 1, 1)
        self.tools_grid.addWidget(QWidget(), 1, i + 1, 1, 1)
        self.tools_grid.addWidget(QWidget(), 2, 0, 1, 1)
        self.tools_grid.setRowStretch(3, 1)
        self.tab0.setLayout(self.tools_grid)

    def instantiate_module(self, module):
        """Instantiates a chosen module class."""
        obj = module(self)
        # Check how many instances of same class already exist
        nInst = sum([item.menu_name == obj.menu_name for item in self.instances_list])
        obj.name += '_' + str(nInst)
        obj.run()
        self.instances_list.append(obj)

    def open_file(self, filename):
        ''' Open file and store it as a Pandas Dataframe.'''
        if filename is None:
            filename, ftype = QFileDialog.getOpenFileName(None, 'Open file', '', "(*.csv)")
        if ftype == '(*.csv)':
            self.file_path = filename
            self.setWindowTitle('PandasVIS - ' + os.path.split(os.path.abspath(self.file_path))[1])
            # Load primary variables
            self.df = pd.read_csv(self.file_path)
            self.primary_names = self.df.keys().tolist()
            # Reset secondary variables
            self.secondary_vars = {'var 3': np.zeros(100), 'var 4': np.zeros(100)}
            self.secondary_names = list(self.secondary_vars.keys())
            # Reset GUI
            self.init_trees()
            self.init_console()

    def init_trees(self):
        ''' Draw hierarchical tree of fields in NWB file '''
        self.tree_primary.clear()
        self.tree_secondary.clear()
        for var1 in self.primary_names:  # primary variables list
            parent = QTreeWidgetItem(self.tree_primary, [var1, str(self.df[var1].dtype)])
            parent.setFlags(parent.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
            parent.setCheckState(0, QtCore.Qt.Checked)
        for var2 in self.secondary_names:  # secondary variables list
            parent = QTreeWidgetItem(self.tree_secondary, [var2, str(self.secondary_vars[var2].dtype)])
            parent.setFlags(parent.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
            parent.setCheckState(0, QtCore.Qt.Checked)

    def init_console(self):
        ''' Initialize commands on console '''
        self.console._execute("import pandas as pd", True)
        self.console._execute("import numpy as np", True)
        self.console._execute("import matplotlib.pyplot as plt", True)
        self.console.push_vars({'df': self.df})
        self.console.push_vars({'secondary_vars': self.secondary_vars})
        self.console.clear()
        self.console.print_text('df --> Dataframe with Primary variables\n')
        self.console.print_text('secondary_vars --> Dictionary with Secondary variables\n\n')

    def new_tab_top(self, object, title):
        """Opens new tab."""
        self.tabs_top.addTab(object, title)
        nTabs = self.tabs_top.children()[0].count()
        self.tabs_top.setCurrentIndex(nTabs - 1)

    def new_tab_bottom(self, tab_object, title):
        """Opens new tab."""
        self.tabs_bottom.addTab(tab_object, title)

    def close_tab_top(self, object):
        """Closes tab and removes associated objects"""
        name = object.name
        # Closes all child Threads
        object.close_threads()
        # Removes tab
        curr_ind = self.tabs_top.children()[0].currentIndex()
        self.tabs_top.removeTab(curr_ind)
        # Removes specific object instance from list
        self.instances_list.remove(object)
        # Deletes object form memory
        object.deleteLater()
        self.write_to_logger(name + ' deleted!')

    def write_to_logger(self, txt):
        time = datetime.datetime.now().time().strftime("%H:%M:%S")
        full_txt = "[" + time + "]    " + txt
        self.logger.append(full_txt)

    def toggle_max_figure(self):
        if self.max_fig:
            self.left_widget.setMaximumWidth(1000)
            self.left_widget.resize(self.left_widget.sizeHint())
            self.tabs_bottom.setMaximumHeight(1000)
            self.tabs_bottom.resize(self.tabs_bottom.sizeHint())
            self.max_fig = False
        else:
            self.left_widget.setMaximumWidth(0)
            self.tabs_bottom.setMaximumHeight(0)
            self.max_fig = True

    def mark_all(self):
        """Iterate over all nodes of the tree and marks them."""
        self.iterator = QTreeWidgetItemIterator(self.tree_primary, QTreeWidgetItemIterator.All)
        while self.iterator.value():
            item = self.iterator.value()
            item.setCheckState(0, QtCore.Qt.Checked)
            self.iterator += 1

    def unmark_all(self):
        """Iterate over all nodes of the tree and unmarks them."""
        self.iterator = QTreeWidgetItemIterator(self.tree_primary, QTreeWidgetItemIterator.All)
        while self.iterator.value():
            item = self.iterator.value()
            item.setCheckState(0, QtCore.Qt.Unchecked)
            self.iterator += 1

    def update_selected_primary(self):
        """Iterate over all nodes of the tree and save selected items names to list"""
        self.selected_primary = []
        self.iterator = QTreeWidgetItemIterator(self.tree_primary, QTreeWidgetItemIterator.All)
        while self.iterator.value():
            item = self.iterator.value()
            if item.checkState(0) == 2:  # full-box checked, add item to dictionary
                self.selected_primary.append(item.text(0))
            self.iterator += 1

    def update_selected_secondary(self):
        """Iterate over all nodes of the tree and save selected items names to list"""
        self.selected_secondary = []
        self.iterator = QTreeWidgetItemIterator(self.tree_secondary, QTreeWidgetItemIterator.All)
        while self.iterator.value():
            item = self.iterator.value()
            if item.checkState(0) == 2:  # full-box checked, add item to dictionary
                self.selected_secondary.append(item.text(0))
            self.iterator += 1

    def to_primary(self):
        self.iterator = QTreeWidgetItemIterator(self.tree_secondary, QTreeWidgetItemIterator.All)
        selected = []
        while self.iterator.value():
            item = self.iterator.value()
            if item.checkState(0) == 2:  # full-box checked
                selected.append(item.text(0))
            self.iterator += 1
        for var in selected:
            move_to_primary(self, var)

    def to_secondary(self):
        self.iterator = QTreeWidgetItemIterator(self.tree_primary, QTreeWidgetItemIterator.All)
        selected = []
        while self.iterator.value():
            item = self.iterator.value()
            if item.checkState(0) == 2:  # full-box checked
                selected.append(item.text(0))
            self.iterator += 1
        for var in selected:
            move_to_secondary(self, var)

    def insert_from_file():
        filename, ftype = QFileDialog.getOpenFileName(None, 'Open file', '', "(*.csv)")
        if ftype == '(*.csv)':
            self.file_path = filename
            # Load primary variables
            df_new = pd.read_csv(self.file_path)
            self.primary_names = self.df.keys().tolist()

    def closeEvent(self, event):
        """Before exiting, deletes temporary files."""
        shutil.rmtree(self.temp_dir, ignore_errors=False, onerror=None)
        event.accept()

    def about(self):
        """About dialog."""
        msg = QMessageBox()
        msg.setWindowTitle("About PandasVIS")
        msg.setIcon(QMessageBox.Information)
        msg.setText("Version: 1.0.0 \n"
                    "Data exploration GUI, with Data Science and Machine Learning embedded tools.\n ")
        msg.setInformativeText("<a href='https://github.com/luiztauffer/pandasVIS'>PandasVIS Github page</a>")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)   # instantiate a QtGui (holder for the app)
    if len(sys.argv) == 1:
        fname = None
    else:
        fname = sys.argv[1]
    ex = Application(filename=fname)
    sys.exit(app.exec_())


def main(filename=None):  # If it was imported as a module
    """Sets up QT application."""
    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)   # instantiate a QtGui (holder for the app)
    ex = Application(filename=filename)
    sys.exit(app.exec_())
