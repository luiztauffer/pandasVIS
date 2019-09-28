from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QMainWindow, QPushButton, QWidget, QGridLayout,
                             QStyle, QGroupBox, QLineEdit, QCheckBox,
                             QVBoxLayout, QHBoxLayout, QLabel, QColorDialog,
                             QComboBox)
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
        self.resize(600, 600)
        self.parent = parent

        self.onlyInt = QtGui.QIntValidator()
        all_fonts = ["Arial", "Balto", "Courier New", "Droid Sans",
                     "Droid Serif", "Droid Sans Mono", "Gravitas One",
                     "Old Standard TT", "Open Sans", "Overpass",
                     "PT Sans Narrow", "Raleway", "Times New Roman"]

        self.bt_uplayout = QPushButton('Update layout')
        self.bt_uplayout.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
        self.bt_uplayout.clicked.connect(self.layout_update)

        self.bt_close = QPushButton('Close')
        self.bt_close.setIcon(self.style().standardIcon(QStyle.SP_DialogCloseButton))
        #self.bt_close.clicked.connect(self.choose_font)

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.bt_uplayout)
        self.hbox.addWidget(self.bt_close)
        self.hbox.addWidget(QWidget())
        self.hbox.addStretch()

        # Overal Layout parameters
        self.lbl_layhover = QLabel('hovermode:')
        self.combo_layhover = QComboBox()
        self.combo_layhover.addItem('closest')
        self.combo_layhover.addItem('x')
        self.combo_layhover.addItem('y')
        self.combo_layhover.addItem('False')
        self.chk_layautosize = QCheckBox('autosize')
        self.lbl_laywidth = QLabel('width:')
        self.lin_laywidth = QLineEdit('700')
        self.lin_laywidth.setValidator(self.onlyInt)
        self.lbl_layheight = QLabel('height:')
        self.lin_layheight = QLineEdit('450')
        self.lin_layheight.setValidator(self.onlyInt)
        self.lbl_layfont = QLabel('font:')
        self.combo_layfont = QComboBox()
        for ft in all_fonts:
            self.combo_layfont.addItem(ft)
        self.lin_layfont = QLineEdit('10')
        self.lin_layfont.setValidator(self.onlyInt)
        self.lbl_layfontc = QLabel('font color (r,g,b,a):')
        self.btn_layfontc = QPushButton('Pick')
        self.btn_layfontc.clicked.connect(lambda: self.choose_color(target='layout_font'))
        self.lin_layfontr = QLineEdit('0')
        self.lin_layfontr.setValidator(self.onlyInt)
        self.lin_layfontg = QLineEdit('0')
        self.lin_layfontg.setValidator(self.onlyInt)
        self.lin_layfontb = QLineEdit('0')
        self.lin_layfontb.setValidator(self.onlyInt)
        self.lin_layfonta = QLineEdit('255')
        self.lin_layfonta.setValidator(self.onlyInt)
        self.lbl_laypaperc = QLabel('paper color (r,g,b,a):')
        self.btn_laypaperc = QPushButton('Pick')
        self.btn_laypaperc.clicked.connect(lambda: self.choose_color(target='layout_paper'))
        self.lin_laypaperr = QLineEdit('255')
        self.lin_laypaperr.setValidator(self.onlyInt)
        self.lin_laypaperg = QLineEdit('255')
        self.lin_laypaperg.setValidator(self.onlyInt)
        self.lin_laypaperb = QLineEdit('255')
        self.lin_laypaperb.setValidator(self.onlyInt)
        self.lin_laypapera = QLineEdit('255')
        self.lin_laypapera.setValidator(self.onlyInt)
        self.lbl_layplotc = QLabel('plot_bg color (r,g,b,a):')
        self.btn_layplotc = QPushButton('Pick')
        self.btn_layplotc.clicked.connect(lambda: self.choose_color(target='layout_plot'))
        self.lin_layplotr = QLineEdit('255')
        self.lin_layplotr.setValidator(self.onlyInt)
        self.lin_layplotg = QLineEdit('255')
        self.lin_layplotg.setValidator(self.onlyInt)
        self.lin_layplotb = QLineEdit('255')
        self.lin_layplotb.setValidator(self.onlyInt)
        self.lin_layplota = QLineEdit('255')
        self.lin_layplota.setValidator(self.onlyInt)
        self.chk_legend = QCheckBox('show legend')

        self.general_grid = QGridLayout()
        self.general_grid.setColumnStretch(7, 1)
        self.general_grid.addWidget(self.lbl_layhover, 0, 0, 1, 1)
        self.general_grid.addWidget(self.combo_layhover, 0, 1, 1, 1)
        self.general_grid.addWidget(self.chk_layautosize, 1, 0, 1, 1)
        self.general_grid.addWidget(self.lbl_laywidth, 2, 0, 1, 1)
        self.general_grid.addWidget(self.lin_laywidth, 2, 1, 1, 1)
        self.general_grid.addWidget(self.lbl_layheight, 3, 0, 1, 1)
        self.general_grid.addWidget(self.lin_layheight, 3, 1, 1, 1)
        self.general_grid.addWidget(self.lbl_layfont, 4, 0, 1, 1)
        self.general_grid.addWidget(self.lin_layfont, 4, 1, 1, 1)
        self.general_grid.addWidget(self.combo_layfont, 4, 2, 1, 2)
        self.general_grid.addWidget(self.lbl_layfontc, 5, 0, 1, 1)
        self.general_grid.addWidget(self.lin_layfontr, 5, 1, 1, 1)
        self.general_grid.addWidget(self.lin_layfontg, 5, 2, 1, 1)
        self.general_grid.addWidget(self.lin_layfontb, 5, 3, 1, 1)
        self.general_grid.addWidget(self.lin_layfonta, 5, 4, 1, 1)
        self.general_grid.addWidget(self.btn_layfontc, 5, 5, 1, 1)
        self.general_grid.addWidget(self.lbl_laypaperc, 6, 0, 1, 1)
        self.general_grid.addWidget(self.lin_laypaperr, 6, 1, 1, 1)
        self.general_grid.addWidget(self.lin_laypaperg, 6, 2, 1, 1)
        self.general_grid.addWidget(self.lin_laypaperb, 6, 3, 1, 1)
        self.general_grid.addWidget(self.lin_laypapera, 6, 4, 1, 1)
        self.general_grid.addWidget(self.btn_laypaperc, 6, 5, 1, 1)
        self.general_grid.addWidget(self.lbl_layplotc, 7, 0, 1, 1)
        self.general_grid.addWidget(self.lin_layplotr, 7, 1, 1, 1)
        self.general_grid.addWidget(self.lin_layplotg, 7, 2, 1, 1)
        self.general_grid.addWidget(self.lin_layplotb, 7, 3, 1, 1)
        self.general_grid.addWidget(self.lin_layplota, 7, 4, 1, 1)
        self.general_grid.addWidget(self.btn_layplotc, 7, 5, 1, 1)
        self.general_grid.addWidget(self.chk_legend, 8, 0, 1, 1)
        self.general_grid.addWidget(QWidget(), 9, 0, 1, 7)

        self.general_group = CollapsibleBox(title='General', parent=self)
        self.general_group.setContentLayout(self.general_grid)


        # Title parameters
        self.lbl_titletext = QLabel('text:')
        self.lin_titletext = QLineEdit('')
        self.lbl_titlefont = QLabel('font:')
        self.combo_titlefont = QComboBox()
        for ft in all_fonts:
            self.combo_titlefont.addItem(ft)
        self.lin_titlefont = QLineEdit('18')
        self.lin_titlefont.setValidator(self.onlyInt)
        self.lbl_titlec = QLabel('color (r,g,b,a):')
        self.btn_titlec = QPushButton('Pick')
        self.btn_titlec.clicked.connect(lambda: self.choose_color(target='title'))
        self.lin_titler = QLineEdit('0')
        self.lin_titler.setValidator(self.onlyInt)
        self.lin_titleg = QLineEdit('0')
        self.lin_titleg.setValidator(self.onlyInt)
        self.lin_titleb = QLineEdit('0')
        self.lin_titleb.setValidator(self.onlyInt)
        self.lin_titlea = QLineEdit('0')
        self.lin_titlea.setValidator(self.onlyInt)

        self.title_grid = QGridLayout()
        self.title_grid.setColumnStretch(7, 1)
        self.title_grid.addWidget(self.lbl_titletext, 0, 0, 1, 1)
        self.title_grid.addWidget(self.lin_titletext, 0, 1, 1, 3)
        self.title_grid.addWidget(self.lbl_titlefont, 1, 0, 1, 1)
        self.title_grid.addWidget(self.lin_titlefont, 1, 1, 1, 1)
        self.title_grid.addWidget(self.combo_titlefont, 1, 2, 1, 2)
        self.title_grid.addWidget(self.lbl_titlec, 2, 0, 1, 1)
        self.title_grid.addWidget(self.lin_titler, 2, 1, 1, 1)
        self.title_grid.addWidget(self.lin_titleg, 2, 2, 1, 1)
        self.title_grid.addWidget(self.lin_titleb, 2, 3, 1, 1)
        self.title_grid.addWidget(self.lin_titlea, 2, 4, 1, 1)
        self.title_grid.addWidget(self.btn_titlec, 2, 5, 1, 1)

        self.title_group = CollapsibleBox(title='Title', parent=self)
        self.title_group.setContentLayout(self.title_grid)

        # X Axis parameters
        self.lbl_xtitle = QLabel('x title')
        self.lin_xtitle = QLineEdit('')

        self.xaxis_grid = QGridLayout()
        self.xaxis_grid.setColumnStretch(7, 1)
        self.xaxis_grid.addWidget(self.lbl_xtitle, 0, 0, 1, 1)
        self.xaxis_grid.addWidget(self.lin_xtitle, 0, 1, 1, 2)

        self.xaxis_group = CollapsibleBox(title='X Axis', parent=self)
        self.xaxis_group.setContentLayout(self.xaxis_grid)

        # Y Axis parameters
        self.lbl_ytitle = QLabel('y title')
        self.lin_ytitle = QLineEdit('')

        self.yaxis_grid = QGridLayout()
        self.yaxis_grid.setColumnStretch(7, 1)
        self.yaxis_grid.addWidget(self.lbl_ytitle, 0, 0, 1, 1)
        self.yaxis_grid.addWidget(self.lin_ytitle, 0, 1, 1, 2)

        self.yaxis_group = CollapsibleBox(title='Y Axis', parent=self)
        self.yaxis_group.setContentLayout(self.yaxis_grid)

        # Main window layout
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.general_group)
        self.vbox.addWidget(self.title_group)
        self.vbox.addWidget(self.xaxis_group)
        self.vbox.addWidget(self.yaxis_group)
        self.vbox.addStretch()
        self.vbox.addLayout(self.hbox)

        centralWidget = QWidget()
        centralWidget.setLayout(self.vbox)
        self.setCentralWidget(centralWidget)
        self.show()

        self.init_attributes()

        self.general_group.toggle_button.click()
        #self.title_group.toggle_button.click()
        #self.xaxis_group.toggle_button.click()
        #self.yaxis_group.toggle_button.click()

    def choose_color(self, target):
        color = QColorDialog.getColor()
        if color.isValid():
            if target=='title':
                self.lin_titler.setText(str(color.red()))
                self.lin_titleg.setText(str(color.green()))
                self.lin_titleb.setText(str(color.blue()))
            elif target=='layout_font':
                self.lin_layfontr.setText(str(color.red()))
                self.lin_layfontg.setText(str(color.green()))
                self.lin_layfontb.setText(str(color.blue()))
            elif target=='layout_paper':
                self.lin_laypaperr.setText(str(color.red()))
                self.lin_laypaperg.setText(str(color.green()))
                self.lin_laypaperb.setText(str(color.blue()))
            elif target=='layout_plot':
                self.lin_layplotr.setText(str(color.red()))
                self.lin_layplotg.setText(str(color.green()))
                self.lin_layplotb.setText(str(color.blue()))

    def layout_update(self):
        """Reads fields and updates parent's layout"""
        changes = AutoDictionary()

        # General
        if str(self.combo_layhover.currentText()) == 'False':
            changes['hovermode'] = False
        else:
            changes['hovermode'] = str(self.combo_layhover.currentText())
        changes['autosize'] = self.chk_layautosize.isChecked()
        changes['width'] = int(self.lin_laywidth.text())
        changes['height'] = int(self.lin_layheight.text())
        changes['font']['family'] = str(self.combo_layfont.currentText())
        changes['font']['size'] = int(self.lin_layfont.text())
        r = str(self.lin_layfontr.text())
        g = str(self.lin_layfontg.text())
        b = str(self.lin_layfontb.text())
        a = str(self.lin_layfonta.text())
        changes['font']['color'] = 'rgb('+r+','+g+','+b+','+a+')'
        r = str(self.lin_laypaperr.text())
        g = str(self.lin_laypaperg.text())
        b = str(self.lin_laypaperb.text())
        a = str(self.lin_laypapera.text())
        changes['paper_bgcolor'] = 'rgb('+r+','+g+','+b+','+a+')'
        r = str(self.lin_layplotr.text())
        g = str(self.lin_layplotg.text())
        b = str(self.lin_layplotb.text())
        a = str(self.lin_layplota.text())
        changes['plot_bgcolor'] = 'rgb('+r+','+g+','+b+','+a+')'
        changes['showlegend'] = self.chk_legend.isChecked()

        # Title
        changes['title']['text'] = str(self.lin_titletext.text())
        changes['title']['font']['family'] = str(self.combo_titlefont.currentText())
        changes['title']['font']['size'] = int(self.lin_titlefont.text())
        r = str(self.lin_titler.text())
        g = str(self.lin_titleg.text())
        b = str(self.lin_titleb.text())
        a = str(self.lin_titlea.text())
        changes['title']['font']['color'] = 'rgb('+r+','+g+','+b+','+a+')'

        # Run layout update
        self.parent.layout_update(changes=changes)

    def init_attributes(self):
        pass
