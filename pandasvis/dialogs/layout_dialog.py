from PyQt5 import QtCore
from PyQt5.QtWidgets import (QMainWindow, QPushButton, QWidget, QGridLayout,
                             QStyle, QFontDialog, QGroupBox, QLineEdit,
                             QVBoxLayout, QLabel, QColorDialog)
from pandasvis.utils.classes import CollapsibleBox
from pandasvis.utils.functions import AutoDictionary


class LayoutDialog(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Layout for " + parent.name)
        self.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint |
            QtCore.Qt.WindowCloseButtonHint
        )
        self.parent = parent

        self.bt_uplayout = QPushButton('Update layout')
        self.bt_uplayout.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
        self.bt_uplayout.clicked.connect(self.layout_update)

        self.bt_close = QPushButton('Close')
        self.bt_close.setIcon(self.style().standardIcon(QStyle.SP_DialogCloseButton))
        #self.bt_close.clicked.connect(self.choose_font)

        # Title parameters
        self.lbl_titletext = QLabel('text:')
        self.lin_titletext = QLineEdit('')
        self.lbl_titlefont = QLabel('font:')
        self.btn_titlefont = QPushButton('Choose')
        self.btn_titlefont.clicked.connect(lambda: self.choose_font(target='title'))
        self.btn_titlecolor = QPushButton('Color')
        self.btn_titlecolor.clicked.connect(lambda: self.choose_color(target='title'))

        self.title_grid = QGridLayout()
        self.title_grid.setColumnStretch(3, 1)
        self.title_grid.addWidget(self.lbl_titletext, 0, 0, 1, 1)
        self.title_grid.addWidget(self.lin_titletext, 0, 1, 1, 3)
        self.title_grid.addWidget(self.lbl_titlefont, 1, 0, 1, 1)
        self.title_grid.addWidget(self.btn_titlefont, 1, 1, 1, 1)
        self.title_grid.addWidget(self.btn_titlecolor, 1, 2, 1, 1)

        self.title_group = CollapsibleBox(title='Title', parent=self)
        self.title_group.setContentLayout(self.title_grid)

        # X Axis parameters
        self.lbl_xtitle = QLabel('x title')
        self.lin_xtitle = QLineEdit('')

        self.xaxis_grid = QGridLayout()
        self.xaxis_grid.setColumnStretch(3, 1)
        self.xaxis_grid.addWidget(self.lbl_xtitle, 0, 0, 1, 1)
        self.xaxis_grid.addWidget(self.lin_xtitle, 0, 1, 1, 2)

        self.xaxis_group = CollapsibleBox(title='X Axis', parent=self)
        self.xaxis_group.setContentLayout(self.xaxis_grid)

        # Y Axis parameters
        self.lbl_ytitle = QLabel('y title')
        self.lin_ytitle = QLineEdit('')

        self.yaxis_grid = QGridLayout()
        self.yaxis_grid.setColumnStretch(3, 1)
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

        self.title_group.toggle_button.click()
        self.xaxis_group.toggle_button.click()
        self.yaxis_group.toggle_button.click()

    def choose_font(self, target):
        font, ok = QFontDialog.getFont()
        if ok:
            atts = font.key().split(',')
            f_family = atts[0]
            f_size = atts[1]
            f_style = atts[-1]
            if target=='title':
                self.title_family = f_family
                self.title_size = f_size

    def choose_color(self, target):
        color = QColorDialog.getColor()
        if color.isValid():
            red = color.red()
            green = color.green()
            blue = color.blue()
            alpha = color.alpha()
            rgb_color = 'rgb('+str(red)+','+str(green)+','+str(blue)+','+str(alpha)+')'
            if target=='title':
                self.title_color = rgb_color

    def layout_update(self):
        """Reads fields and updates parent's layout"""
        changes = AutoDictionary()
        changes['title']['text'] = self.lin_titletext.text()
        changes['title']['font']['family'] = self.title_family
        changes['title']['font']['size'] = self.title_size
        changes['title']['font']['color'] = self.title_color
        self.parent.layout_update(changes=changes)
