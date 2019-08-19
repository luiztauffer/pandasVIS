from PyQt5 import QtCore, QtGui, Qt
from PyQt5.QtWidgets import (QWidget, QApplication, QTreeWidget, QTreeWidgetItem,
    QMainWindow, QFileDialog, QAction, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QTreeWidgetItemIterator, QTabWidget)
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
from pandasvis.classes.QTreeCustom import QTreeCustomPrimary

from console_widget import ConsoleWidget
import numpy as np
import pandas as pd
import pandas_profiling
import os
import sys
import shutil

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
        self.tree_primary = QTreeCustomPrimary() #QTreeWidget()
        self.tree_primary.setHeaderLabels(['Primary Variables'])
        #self.tree_primary.itemClicked.connect(self.onItemClicked)
        self.tree_secondary = QTreeWidget()
        self.tree_secondary.setHeaderLabels(['Secondary Variables'])
        #self.tree_secondary.itemClicked.connect(self.onItemClicked)

        self.primary_names = ['name 1', 'name 2']
        self.init_trees()

        self.grid_left1 = QGridLayout()
        self.grid_left1.addWidget(self.tree_primary, 0, 0, 1, 6)
        self.grid_left1.addWidget(self.tree_secondary, 1, 0, 1, 6)

         # Center panels -------------------------------------------------------
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        #self.tabs.resize(600,600)
        self.tabs.addTab(self.tab1,"Overview")
        self.tabs.addTab(self.tab2,"Tab 2")
         # Create first tab
        self.tab1.layout = QVBoxLayout()
        self.webview = QWebEngineView()
        self.tab1.layout.addWidget(self.webview)
        self.tab1.setLayout(self.tab1.layout)
        #self.refresh_tab1()

        self.console = ConsoleWidget(par=self)

        self.vbox1 = QVBoxLayout()
        self.vbox1.addWidget(self.tabs)
        self.vbox1.addWidget(self.console)

        self.hbox = QHBoxLayout(self.centralwidget)
        self.hbox.addLayout(self.grid_left1)      #add left panel
        self.hbox.addLayout(self.vbox1)    #add centre panel


    def open_file(self, filename):
        ''' Open file and store it as a Pandas Dataframe.'''
        if filename is None:
            filename, ftype = QFileDialog.getOpenFileName(None, 'Open file', '', "(*.csv)")
        if ftype=='(*.csv)':
            self.file_path = filename
            self.df = pd.read_csv(self.file_path)
            self.primary_names = self.df.keys().tolist()
            self.df_profile = self.df.profile_report(title='Summary Report', style={'full_width':True}, )
            self.df_profile.to_file(os.path.join(self.temp_dir,'summary_report.html'), silent=True)
            self.setWindowTitle('PandasVIS - '+os.path.split(os.path.abspath(self.file_path))[1])
            self.init_trees()
            self.init_console()
            self.refresh_tab1()

    def init_trees(self):
        ''' Draw hierarchical tree of fields in NWB file '''
        self.tree_primary.clear()
        self.tree_secondary.clear()
        for var1 in self.primary_names:  #primary variables list
            parent = QTreeWidgetItem(self.tree_primary)
            parent.setText(0, var1)
            parent.setFlags(parent.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
            parent.setCheckState(0, QtCore.Qt.Checked)

    def init_console(self):
        ''' Initialize commands on console '''
        self.console._execute("import pandas as pd", True)
        self.console._execute("import numpy as np", True)
        self.console._execute("import matplotlib.pyplot as plt", True)
        self.console.push_vars({'df':self.df})
        self.console.clear()

    def refresh_tab1(self):
        url = QtCore.QUrl.fromLocalFile(os.path.join(self.temp_dir,'summary_report.html'))
        self.webview.load(url)
        self.webview.show()

    def onItemClicked(self, it, col):
        if self.auto_clear:  #clears terminal
            self.console.clear()
        if it.parent() is not None: #2nd level groups (at least)
            field1 = it.parent().text(0)
            field0 = it.text(0)
            if it.parent().parent() is not None: #3rd level groups
                field2 = it.parent().parent().text(0)
                if field1=='ecephys':
                    item = self.nwb.fields[field2][field1].data_interfaces[field0]
            else:
                field2 = None
                item = self.nwb.fields[field1][field0]
        else: #1st level groups ('acquisition','electrodes', etc...)
            field2 = None
            field1 = None
            field0 = it.text(0)
            item = self.nwb.fields[field0]
        self.console.push_vars({'tree':self.tree})
        self.console.push_vars({'item':item})
        self.console._execute("print(item)", False)

    def find_selected_items(self):
        """Iterate over all children of the tree and save selected items to dictionary."""
        self.cp_objs = {}
        self.iterator = QTreeWidgetItemIterator(self.tree, QTreeWidgetItemIterator.All)
        while self.iterator.value():
            item = self.iterator.value()
            if item.checkState(0)==2: #full-box checked, add item to dictionary
                if item.parent() is not None: #2nd level item (at least)
                    if item.parent().text(0) in self.cp_objs:  #append if parent already present as key in dictionary
                        if self.cp_objs[item.parent().text(0)]==True: #remove boolean parent key:value
                            self.cp_objs.pop(item.parent().text(0), None)
                            self.cp_objs[item.parent().text(0)] = [item.text(0)]
                        else:
                            self.cp_objs[item.parent().text(0)].append(item.text(0))
                    else: #add new list with item, if parent not yet a key in dictionary
                        self.cp_objs[item.parent().text(0)] = [item.text(0)]
                else:  #1st level item
                    self.cp_objs[item.text(0)] = True
            self.iterator += 1
        self.console.push_vars({'cp_objs':self.cp_objs})

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
