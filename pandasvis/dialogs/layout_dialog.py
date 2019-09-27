from PyQt5.QtWidgets import (QMainWindow, QPushButton, QWidget, QGridLayout,
                             QStyle, QFontDialog, QGroupBox, QLineEdit,
                             QVBoxLayout, QLabel)
from pandasvis.utils.classes import CollapsibleBox


class LayoutDialog(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Layout for " + parent.name)
        self.parent = parent

        self.bt_uplayout = QPushButton('Update layout')
        self.bt_uplayout.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
        self.bt_uplayout.clicked.connect(self.layout_update)

        self.bt_close = QPushButton('Close')
        self.bt_close.setIcon(self.style().standardIcon(QStyle.SP_DialogCloseButton))
        self.bt_close.clicked.connect(self.choose_font)

        # Title parameters
        self.lbl_text = QLabel('text:')
        self.lin_text = QLineEdit('')

        self.title_grid = QGridLayout()
        self.title_grid.addWidget(self.lbl_text, 0, 0, 1, 1)
        self.title_grid.addWidget(self.lin_text, 0, 1, 1, 2)

        self.title_group = CollapsibleBox(title='Title', parent=self)
        self.title_group.setContentLayout(self.title_grid)

        # X Axis parameters
        self.lbl_xtitle = QLabel('x title')
        self.lin_xtitle = QLineEdit('')

        self.xaxis_grid = QGridLayout()
        self.xaxis_grid.addWidget(self.lbl_xtitle, 0, 0, 1, 1)
        self.xaxis_grid.addWidget(self.lin_xtitle, 0, 1, 1, 2)

        self.xaxis_group = CollapsibleBox(title='X Axis', parent=self)
        self.xaxis_group.setContentLayout(self.xaxis_grid)

        # Y Axis parameters
        self.lbl_ytitle = QLabel('y title')
        self.lin_ytitle = QLineEdit('')

        self.yaxis_grid = QGridLayout()
        self.yaxis_grid.addWidget(self.lbl_ytitle, 0, 0, 1, 1)
        self.yaxis_grid.addWidget(self.lin_ytitle, 0, 1, 1, 2)

        self.yaxis_group = CollapsibleBox(title='Y Axis', parent=self)
        self.yaxis_group.setContentLayout(self.yaxis_grid)

        # Main window layout
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.title_group)
        self.vbox.addWidget(self.xaxis_group)
        self.vbox.addWidget(self.yaxis_group)
        self.vbox.addStretch()

        centralWidget = QWidget()
        centralWidget.setLayout(self.vbox)
        self.setCentralWidget(centralWidget)
        self.show()

    def choose_font(self):
        w = QFontDialog()
        print(w)

    def layout_update(self):
        """Reads fields and updates parent's layout"""
        pass
