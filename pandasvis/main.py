from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QApplication, QTreeWidget, QTreeWidgetItem,
    QMainWindow, QFileDialog, QAction, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QTreeWidgetItemIterator, QTabWidget, QSplitter)
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
from pandasvis.classes.QTreeCustom import QTreeCustomPrimary, QTreeCustomSecondary
from pandasvis.classes.console_widget import ConsoleWidget
from pandasvis.classes.cufflinks_subs import custom_scatter_matrix
from pandasvis.classes.dialogs_filter import FilterVariablesDialog
import numpy as np
import pandas as pd
import pandas_profiling
import os
import sys
import shutil

from plotly.offline import plot as ptl_plot
import cufflinks as cf
cf.go_offline()

class Application(QMainWindow):
    def __init__(self, filename):
        super().__init__()

        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.resize(1200, 900)
        self.setWindowTitle('PandasVIS')

        #Initialize GUI elements
        self.init_gui()

        # Opens file (if argument was passed)
        if filename is not None:
            self.open_file()

        # Creates temp folder for temporary files
        self.temp_dir = os.path.join(os.getcwd(),'temp')
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir, exist_ok=True)

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

        toolsMenu = mainMenu.addMenu('Tools')
        action_func1 = QAction('Func 1', self)
        toolsMenu.addAction(action_func1)
        #action_load_annotations.triggered.connect(self.load_annotations)
        action_func2 = QAction('Func 2', self)
        toolsMenu.addAction(action_func2)
        #action_load_intervals.triggered.connect(self.load_intervals)

        helpMenu = mainMenu.addMenu('Help')
        action_about = QAction('About', self)
        helpMenu.addAction(action_about)
        #action_about.triggered.connect(self.about)

        # Left panels ----------------------------------------------------------
        self.bt_refreshOverview = QPushButton('Overview')
        self.bt_refreshOverview.clicked.connect(lambda: self.refresh_overview())
        self.bt_refreshOverview.setToolTip("Refresh Overview")
        self.bt_scatterMatrix = QPushButton('Scatter matrix')
        self.bt_scatterMatrix.clicked.connect(lambda: self.make_scatter_matrix())
        self.bt_scatterMatrix.setToolTip("Scatter matrix for\nselected variables")

        self.tree_primary = QTreeCustomPrimary(parent=self)
        self.tree_primary.setHeaderLabels(['Primary Variables'])
        self.tree_primary.setToolTip("Columns of the Dataframe. Can be accessed\n"+
                                     "in the console with the variable 'df'")
        self.tree_primary.itemClicked.connect(self.update_selected_primary)
        self.tree_secondary = QTreeCustomSecondary(parent=self)
        self.tree_secondary.setHeaderLabels(['Secondary Variables'])
        self.tree_secondary.setToolTip("Secondary variables, can be added to the Dataframe.\n"
                                       "Can be accessed in the console with the variable \n"+
                                       "'secondary_vars'")
        self.tree_secondary.itemClicked.connect(self.update_selected_secondary)

        self.df = pd.DataFrame(np.random.rand(100, 5), columns=['a', 'b', 'c', 'd', 'e'])
        names = ['aa', 'bb', 'cc']
        nm = [names[ind%3] for ind in np.arange(100)]
        self.df['name'] = nm
        self.primary_names = list(self.df.keys())
        self.secondary_vars = {'var 3':np.zeros(100), 'var 4':np.zeros(100)}
        self.secondary_names = list(self.secondary_vars.keys())
        self.init_trees()

        self.vbox1 = QSplitter(Qt.Vertical)
        self.vbox1.addWidget(self.tree_primary)
        self.vbox1.addWidget(self.tree_secondary)

        self.grid_left1 = QGridLayout()
        self.grid_left1.addWidget(self.bt_refreshOverview, 0, 0, 1, 3)
        self.grid_left1.addWidget(self.bt_scatterMatrix, 0, 3, 1, 3)
        self.grid_left1.addWidget(self.vbox1, 1, 0, 1, 6)
        self.left_widget = QWidget()
        self.left_widget.setLayout(self.grid_left1)


         # Center panels -------------------------------------------------------
        self.tabs = QTabWidget()
        #self.tabs.resize(600,600)
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.addTab(self.tab1,"Overview")
        self.tabs.addTab(self.tab2,"Scatter matrix")
        # Create first tab
        self.tab1.layout = QVBoxLayout()
        self.webview = QWebEngineView()
        self.tab1.layout.addWidget(self.webview)
        self.tab1.setLayout(self.tab1.layout)
        # Create second tab
        self.tab2.layout = QVBoxLayout()
        self.scatter_matrix = QWebEngineView()
        self.tab2.layout.addWidget(self.scatter_matrix)
        self.tab2.setLayout(self.tab2.layout)

        self.console = ConsoleWidget(par=self)

        self.righ_widget = QSplitter(Qt.Vertical)
        self.righ_widget.addWidget(self.tabs)
        self.righ_widget.addWidget(self.console)

        # Window layout --------------------------------------------------------
        #self.hbox = QHBoxLayout(self.centralwidget)
        self.hbox = QSplitter(Qt.Horizontal)
        self.hbox.addWidget(self.left_widget)      #add left panel
        self.hbox.addWidget(self.righ_widget)    #add centre panel
        self.setCentralWidget(self.hbox)

    def open_file(self, filename):
        ''' Open file and store it as a Pandas Dataframe.'''
        if filename is None:
            filename, ftype = QFileDialog.getOpenFileName(None, 'Open file', '', "(*.csv)")
        if ftype=='(*.csv)':
            self.file_path = filename
            self.setWindowTitle('PandasVIS - '+os.path.split(os.path.abspath(self.file_path))[1])
            #Load primary variables
            self.df = pd.read_csv(self.file_path)
            self.primary_names = self.df.keys().tolist()
            #Reset secondary variables
            self.secondary_vars = {'var 3':np.zeros(100), 'var 4':np.zeros(100)}
            self.secondary_names = list(self.secondary_vars.keys())
            #Generates profile report
            self.df_profile = self.df.profile_report(title='Summary Report', style={'full_width':True}, )
            self.df_profile.to_file(os.path.join(self.temp_dir,'summary_report.html'), silent=True)
            #Reset GUI
            self.init_trees()
            self.init_console()
            self.refresh_tab1()
            self.refresh_tab2()

    def init_trees(self):
        ''' Draw hierarchical tree of fields in NWB file '''
        self.tree_primary.clear()
        self.tree_secondary.clear()
        for var1 in self.primary_names:  #primary variables list
            parent = QTreeWidgetItem(self.tree_primary)
            parent.setText(0, var1)
            parent.setFlags(parent.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
            parent.setCheckState(0, QtCore.Qt.Checked)
        for var2 in self.secondary_names:  #secondary variables list
            parent = QTreeWidgetItem(self.tree_secondary)
            parent.setText(0, var2)
            parent.setFlags(parent.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
            parent.setCheckState(0, QtCore.Qt.Checked)

    def init_console(self):
        ''' Initialize commands on console '''
        self.console._execute("import pandas as pd", True)
        self.console._execute("import numpy as np", True)
        self.console._execute("import matplotlib.pyplot as plt", True)
        self.console.push_vars({'df':self.df})
        self.console.clear()
        self.console.print_text('df --> Dataframe with Primary variables\n')
        self.console.print_text('secondary_vars --> Dictionary with Secondary variables\n\n')

    def refresh_tab1(self):
        """Loads temporary HTML file and render it at tab 1"""
        url = QtCore.QUrl.fromLocalFile(os.path.join(self.temp_dir,'summary_report.html'))
        self.webview.load(url)
        self.webview.show()
        self.tabs.setCurrentIndex(0)

    def refresh_overview(self):
        """Produces new profile overview with current df"""
        self.primary_names = self.df.keys().tolist()
        self.df_profile = self.df.profile_report(title='Summary Report', style={'full_width':True}, )
        self.df_profile.to_file(os.path.join(self.temp_dir,'summary_report.html'), silent=True)
        self.refresh_tab1()

    def refresh_tab2(self):
        """Loads temporary HTML file and render it at tab 2"""
        url = QtCore.QUrl.fromLocalFile(os.path.join(self.temp_dir,'scatter_matrix.html'))
        self.scatter_matrix.load(url)
        self.scatter_matrix.show()
        self.tabs.setCurrentIndex(1)

    def make_scatter_matrix(self):
        """Produces new scatter matrix plot with selected variables"""
        #Select variables from Dataframe
        self.update_selected_primary()
        df = self.df[self.selected_primary]
        #Open filter by condition dialog
        w = FilterVariablesDialog(self, df)
        if w.value==1:
            #Generate a dictionary of plotly plots
            a = custom_scatter_matrix(w.df, groupby=w.group_by)
            #Saves html to temporary folder
            ptl_plot(a, filename=os.path.join(self.temp_dir,'scatter_matrix.html'), auto_open=False)
            self.refresh_tab2()

    def update_selected_primary(self):
        """Iterate over all nodes of the tree and save selected items names to list"""
        self.selected_primary = []
        self.iterator = QTreeWidgetItemIterator(self.tree_primary, QTreeWidgetItemIterator.All)
        while self.iterator.value():
            item = self.iterator.value()
            if item.checkState(0) == 2: #full-box checked, add item to dictionary
                self.selected_primary.append(item.text(0))
            self.iterator += 1

    def update_selected_secondary(self):
        """Iterate over all nodes of the tree and save selected items names to list"""
        self.selected_secondary = []
        self.iterator = QTreeWidgetItemIterator(self.tree_secondary, QTreeWidgetItemIterator.All)
        while self.iterator.value():
            item = self.iterator.value()
            if item.checkState(0) == 2: #full-box checked, add item to dictionary
                self.selected_secondary.append(item.text(0))
            self.iterator += 1

    def closeEvent(self, event):
        """Before exiting, deletes temporary files."""
        shutil.rmtree(self.temp_dir, ignore_errors=False, onerror=None)
        event.accept()




if __name__ == '__main__':
    app = QApplication(sys.argv)  #instantiate a QtGui (holder for the app)
    if len(sys.argv)==1:
        fname = None
    else:
        fname = sys.argv[1]
    ex = Application(filename=fname)
    sys.exit(app.exec_())


def main(filename=None):  # If it was imported as a module
    """Sets up QT application."""
    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)  #instantiate a QtGui (holder for the app)
    ex = Application(filename=filename)
    sys.exit(app.exec_())
