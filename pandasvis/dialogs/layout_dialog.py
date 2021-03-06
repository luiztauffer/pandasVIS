from PySide2 import QtCore, QtGui
from PySide2.QtWidgets import (QMainWindow, QPushButton, QWidget, QGridLayout,
                               QStyle, QLineEdit, QCheckBox,
                               QVBoxLayout, QHBoxLayout, QLabel, QColorDialog,
                               QComboBox, QScrollArea)
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

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.bt_uplayout)
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
        self.chk_layautosize.setChecked(True)
        self.chk_layautosize.stateChanged.connect(self.toggle_enable_fields)
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
        self.chk_legend.setChecked(True)

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
        self.lin_titlea = QLineEdit('255')
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
        self.chk_xvisible = QCheckBox('visible')
        self.chk_xvisible.setChecked(True)
        self.lbl_xc = QLabel('color (r,g,b,a):')
        self.btn_xc = QPushButton('Pick')
        self.btn_xc.clicked.connect(lambda: self.choose_color(target='xaxis'))
        self.lin_xr = QLineEdit('255')
        self.lin_xr.setValidator(self.onlyInt)
        self.lin_xg = QLineEdit('255')
        self.lin_xg.setValidator(self.onlyInt)
        self.lin_xb = QLineEdit('255')
        self.lin_xb.setValidator(self.onlyInt)
        self.lin_xa = QLineEdit('255')
        self.lin_xa.setValidator(self.onlyInt)
        self.lbl_xtitletext = QLabel('text:')
        self.lin_xtitletext = QLineEdit('')
        self.lbl_xtitlefont = QLabel('font:')
        self.combo_xtitlefont = QComboBox()
        for ft in all_fonts:
            self.combo_xtitlefont.addItem(ft)
        self.lin_xtitlefont = QLineEdit('10')
        self.lin_xtitlefont.setValidator(self.onlyInt)
        self.lbl_xtitlec = QLabel('font color (r,g,b,a):')
        self.btn_xtitlec = QPushButton('Pick')
        self.btn_xtitlec.clicked.connect(lambda: self.choose_color(target='xaxis_title'))
        self.lin_xtitler = QLineEdit('27')
        self.lin_xtitler.setValidator(self.onlyInt)
        self.lin_xtitleg = QLineEdit('27')
        self.lin_xtitleg.setValidator(self.onlyInt)
        self.lin_xtitleb = QLineEdit('27')
        self.lin_xtitleb.setValidator(self.onlyInt)
        self.lin_xtitlea = QLineEdit('255')
        self.lin_xtitlea.setValidator(self.onlyInt)
        self.lbl_xtype = QLabel('type:')
        self.combo_xtype = QComboBox()
        self.combo_xtype.addItem("-")
        self.combo_xtype.addItem("linear")
        self.combo_xtype.addItem("log")
        self.combo_xtype.addItem("date")
        self.combo_xtype.addItem("category")
        self.combo_xtype.addItem("multicategory")
        self.chk_xautorange = QCheckBox('autorange')
        self.chk_xautorange.setChecked(True)
        self.lbl_xnticks = QLabel('nticks:')
        self.lin_xnticks = QLineEdit('4')
        self.lin_xnticks.setValidator(self.onlyInt)
        self.lbl_xticks = QLabel('ticks:')
        self.combo_xticks = QComboBox()
        self.combo_xticks.addItem("inside")
        self.combo_xticks.addItem("outside")
        self.combo_xticks.addItem("")
        self.lbl_xticklen = QLabel('tick length:')
        self.lin_xticklen = QLineEdit('5')
        self.lin_xticklen.setValidator(self.onlyInt)
        self.lbl_xtickwid = QLabel('tick width:')
        self.lin_xtickwid = QLineEdit('1')
        self.lin_xtickwid.setValidator(self.onlyInt)
        self.lbl_xtickc = QLabel('tick color (r,g,b,a):')
        self.btn_xtickc = QPushButton('Pick')
        self.btn_xtickc.clicked.connect(lambda: self.choose_color(target='xaxis_tick'))
        self.lin_xtickr = QLineEdit('27')
        self.lin_xtickr.setValidator(self.onlyInt)
        self.lin_xtickg = QLineEdit('27')
        self.lin_xtickg.setValidator(self.onlyInt)
        self.lin_xtickb = QLineEdit('27')
        self.lin_xtickb.setValidator(self.onlyInt)
        self.lin_xticka = QLineEdit('255')
        self.lin_xticka.setValidator(self.onlyInt)
        self.chk_xshowticklabels = QCheckBox('show tick labels')
        self.chk_xshowticklabels.setChecked(True)
        self.lbl_xtickangle = QLabel('tick angle:')
        self.chk_xtickangle = QCheckBox('auto')
        self.chk_xtickangle.setChecked(True)
        self.chk_xtickangle.stateChanged.connect(self.toggle_enable_fields)
        self.lin_xtickangle = QLineEdit('0')
        self.lin_xtickangle.setValidator(self.onlyInt)
        self.lbl_xtickprefix = QLabel('tick prefix:')
        self.lin_xtickprefix = QLineEdit('')
        self.combo_xshowtickprefix = QComboBox()
        self.combo_xshowtickprefix.addItem("all")
        self.combo_xshowtickprefix.addItem("first")
        self.combo_xshowtickprefix.addItem("last")
        self.combo_xshowtickprefix.addItem("none")
        self.lbl_xticksufix = QLabel('tick sufix:')
        self.lin_xticksufix = QLineEdit('')
        self.combo_xshowticksufix = QComboBox()
        self.combo_xshowticksufix.addItem("all")
        self.combo_xshowticksufix.addItem("first")
        self.combo_xshowticksufix.addItem("last")
        self.combo_xshowticksufix.addItem("none")
        self.lbl_xexponent = QLabel('exponent:')
        self.combo_xexponent = QComboBox()
        self.combo_xexponent.addItem("B")
        self.combo_xexponent.addItem("e")
        self.combo_xexponent.addItem("E")
        self.combo_xexponent.addItem("power")
        self.combo_xexponent.addItem("SI")
        self.combo_xexponent.addItem("none")
        self.combo_xshowexponent = QComboBox()
        self.combo_xshowexponent.addItem("all")
        self.combo_xshowexponent.addItem("first")
        self.combo_xshowexponent.addItem("last")
        self.combo_xshowexponent.addItem("none")
        self.lbl_xtickformat = QLabel('tick format:')
        self.lin_xtickformat = QLineEdit('')
        self.chk_xshowline = QCheckBox('show line')
        self.chk_xshowline.setChecked(False)
        self.chk_xshowline.stateChanged.connect(self.toggle_enable_fields)
        self.lbl_xlinewid = QLabel('line width:')
        self.lin_xlinewid = QLineEdit('1')
        self.lin_xlinewid.setValidator(self.onlyInt)
        self.lbl_xlinec = QLabel('line color (r,g,b,a):')
        self.btn_xlinec = QPushButton('Pick')
        self.btn_xlinec.clicked.connect(lambda: self.choose_color(target='xaxis_line'))
        self.lin_xliner = QLineEdit('27')
        self.lin_xliner.setValidator(self.onlyInt)
        self.lin_xlineg = QLineEdit('27')
        self.lin_xlineg.setValidator(self.onlyInt)
        self.lin_xlineb = QLineEdit('27')
        self.lin_xlineb.setValidator(self.onlyInt)
        self.lin_xlinea = QLineEdit('255')
        self.lin_xlinea.setValidator(self.onlyInt)
        self.chk_xshowgrid = QCheckBox('show grid')
        self.chk_xshowgrid.setChecked(False)
        self.chk_xshowgrid.stateChanged.connect(self.toggle_enable_fields)
        self.lbl_xgridwid = QLabel('grid width:')
        self.lin_xgridwid = QLineEdit('1')
        self.lin_xgridwid.setValidator(self.onlyInt)
        self.lbl_xgridc = QLabel('grid color (r,g,b,a):')
        self.btn_xgridc = QPushButton('Pick')
        self.btn_xgridc.clicked.connect(lambda: self.choose_color(target='xaxis_grid'))
        self.lin_xgridr = QLineEdit('238')
        self.lin_xgridr.setValidator(self.onlyInt)
        self.lin_xgridg = QLineEdit('238')
        self.lin_xgridg.setValidator(self.onlyInt)
        self.lin_xgridb = QLineEdit('238')
        self.lin_xgridb.setValidator(self.onlyInt)
        self.lin_xgrida = QLineEdit('255')
        self.lin_xgrida.setValidator(self.onlyInt)
        self.chk_xzeroline = QCheckBox('show zero-line')
        self.chk_xzeroline.setChecked(False)
        self.chk_xzeroline.stateChanged.connect(self.toggle_enable_fields)
        self.lbl_xzerolinewid = QLabel('zero-line width:')
        self.lin_xzerolinewid = QLineEdit('1')
        self.lin_xzerolinewid.setValidator(self.onlyInt)
        self.lbl_xzerolinec = QLabel('zero-line color (r,g,b,a):')
        self.btn_xzerolinec = QPushButton('Pick')
        self.btn_xzerolinec.clicked.connect(lambda: self.choose_color(target='xaxis_zeroline'))
        self.lin_xzeroliner = QLineEdit('68')
        self.lin_xzeroliner.setValidator(self.onlyInt)
        self.lin_xzerolineg = QLineEdit('68')
        self.lin_xzerolineg.setValidator(self.onlyInt)
        self.lin_xzerolineb = QLineEdit('68')
        self.lin_xzerolineb.setValidator(self.onlyInt)
        self.lin_xzerolinea = QLineEdit('255')
        self.lin_xzerolinea.setValidator(self.onlyInt)
        self.lbl_xside = QLabel('side:')
        self.combo_xside = QComboBox()
        self.combo_xside.addItem("bottom")
        self.combo_xside.addItem("top")

        self.xaxis_grid = QGridLayout()
        self.xaxis_grid.setColumnStretch(7, 1)
        self.xaxis_grid.addWidget(self.chk_xvisible, 0, 0, 1, 1)
        self.xaxis_grid.addWidget(self.lbl_xc, 1, 0, 1, 1)
        self.xaxis_grid.addWidget(self.lin_xr, 1, 1, 1, 1)
        self.xaxis_grid.addWidget(self.lin_xg, 1, 2, 1, 1)
        self.xaxis_grid.addWidget(self.lin_xb, 1, 3, 1, 1)
        self.xaxis_grid.addWidget(self.lin_xa, 1, 4, 1, 1)
        self.xaxis_grid.addWidget(self.btn_xc, 1, 5, 1, 1)
        self.xaxis_grid.addWidget(self.lbl_xtitletext, 2, 0, 1, 1)
        self.xaxis_grid.addWidget(self.lin_xtitletext, 2, 1, 1, 3)
        self.xaxis_grid.addWidget(self.lbl_xtitlefont, 3, 0, 1, 1)
        self.xaxis_grid.addWidget(self.lin_xtitlefont, 3, 1, 1, 1)
        self.xaxis_grid.addWidget(self.combo_xtitlefont, 3, 2, 1, 2)
        self.xaxis_grid.addWidget(self.lbl_xtitlec, 4, 0, 1, 1)
        self.xaxis_grid.addWidget(self.lin_xtitler, 4, 1, 1, 1)
        self.xaxis_grid.addWidget(self.lin_xtitleg, 4, 2, 1, 1)
        self.xaxis_grid.addWidget(self.lin_xtitleb, 4, 3, 1, 1)
        self.xaxis_grid.addWidget(self.lin_xtitlea, 4, 4, 1, 1)
        self.xaxis_grid.addWidget(self.btn_xtitlec, 4, 5, 1, 1)
        self.xaxis_grid.addWidget(self.lbl_xtype, 5, 0, 1, 1)
        self.xaxis_grid.addWidget(self.combo_xtype, 5, 1, 1, 2)
        self.xaxis_grid.addWidget(self.chk_xautorange, 6, 0, 1, 1)
        self.xaxis_grid.addWidget(self.lbl_xnticks, 7, 0, 1, 1)
        self.xaxis_grid.addWidget(self.lin_xnticks, 7, 1, 1, 1)
        self.xaxis_grid.addWidget(self.lbl_xticks, 8, 0, 1, 1)
        self.xaxis_grid.addWidget(self.combo_xticks, 8, 1, 1, 2)
        self.xaxis_grid.addWidget(self.lbl_xticklen, 9, 0, 1, 1)
        self.xaxis_grid.addWidget(self.lin_xticklen, 9, 1, 1, 1)
        self.xaxis_grid.addWidget(self.lbl_xtickwid, 10, 0, 1, 1)
        self.xaxis_grid.addWidget(self.lin_xtickwid, 10, 1, 1, 1)
        self.xaxis_grid.addWidget(self.lbl_xtickc, 11, 0, 1, 1)
        self.xaxis_grid.addWidget(self.lin_xtickr, 11, 1, 1, 1)
        self.xaxis_grid.addWidget(self.lin_xtickg, 11, 2, 1, 1)
        self.xaxis_grid.addWidget(self.lin_xtickb, 11, 3, 1, 1)
        self.xaxis_grid.addWidget(self.lin_xticka, 11, 4, 1, 1)
        self.xaxis_grid.addWidget(self.btn_xtickc, 11, 5, 1, 1)
        self.xaxis_grid.addWidget(self.chk_xshowticklabels, 12, 0, 1, 1)
        self.xaxis_grid.addWidget(self.lbl_xtickangle, 13, 0, 1, 1)
        self.xaxis_grid.addWidget(self.chk_xtickangle, 13, 1, 1, 1)
        self.xaxis_grid.addWidget(self.lin_xtickangle, 13, 2, 1, 1)
        self.xaxis_grid.addWidget(self.lbl_xtickprefix, 14, 0, 1, 1)
        self.xaxis_grid.addWidget(self.lin_xtickprefix, 14, 1, 1, 1)
        self.xaxis_grid.addWidget(self.combo_xshowtickprefix, 14, 2, 1, 1)
        self.xaxis_grid.addWidget(self.lbl_xticksufix, 15, 0, 1, 1)
        self.xaxis_grid.addWidget(self.lin_xticksufix, 15, 1, 1, 1)
        self.xaxis_grid.addWidget(self.combo_xshowticksufix, 15, 2, 1, 1)
        self.xaxis_grid.addWidget(self.lbl_xexponent, 16, 0, 1, 1)
        self.xaxis_grid.addWidget(self.combo_xexponent, 16, 1, 1, 1)
        self.xaxis_grid.addWidget(self.combo_xshowexponent, 16, 2, 1, 1)
        self.xaxis_grid.addWidget(self.lbl_xtickformat, 17, 0, 1, 1)
        self.xaxis_grid.addWidget(self.lin_xtickformat, 17, 1, 1, 1)
        self.xaxis_grid.addWidget(self.chk_xshowline, 18, 0, 1, 1)
        self.xaxis_grid.addWidget(self.lbl_xlinewid, 19, 0, 1, 1)
        self.xaxis_grid.addWidget(self.lin_xlinewid, 19, 1, 1, 1)
        self.xaxis_grid.addWidget(self.lbl_xlinec, 20, 0, 1, 1)
        self.xaxis_grid.addWidget(self.lin_xliner, 20, 1, 1, 1)
        self.xaxis_grid.addWidget(self.lin_xlineg, 20, 2, 1, 1)
        self.xaxis_grid.addWidget(self.lin_xlineb, 20, 3, 1, 1)
        self.xaxis_grid.addWidget(self.lin_xlinea, 20, 4, 1, 1)
        self.xaxis_grid.addWidget(self.btn_xlinec, 20, 5, 1, 1)
        self.xaxis_grid.addWidget(self.chk_xshowgrid, 21, 0, 1, 1)
        self.xaxis_grid.addWidget(self.lbl_xgridwid, 22, 0, 1, 1)
        self.xaxis_grid.addWidget(self.lin_xgridwid, 22, 1, 1, 1)
        self.xaxis_grid.addWidget(self.lbl_xgridc, 23, 0, 1, 1)
        self.xaxis_grid.addWidget(self.lin_xgridr, 23, 1, 1, 1)
        self.xaxis_grid.addWidget(self.lin_xgridg, 23, 2, 1, 1)
        self.xaxis_grid.addWidget(self.lin_xgridb, 23, 3, 1, 1)
        self.xaxis_grid.addWidget(self.lin_xgrida, 23, 4, 1, 1)
        self.xaxis_grid.addWidget(self.btn_xgridc, 23, 5, 1, 1)
        self.xaxis_grid.addWidget(self.chk_xzeroline, 24, 0, 1, 1)
        self.xaxis_grid.addWidget(self.lbl_xzerolinewid, 25, 0, 1, 1)
        self.xaxis_grid.addWidget(self.lin_xzerolinewid, 25, 1, 1, 1)
        self.xaxis_grid.addWidget(self.lbl_xzerolinec, 26, 0, 1, 1)
        self.xaxis_grid.addWidget(self.lin_xzeroliner, 26, 1, 1, 1)
        self.xaxis_grid.addWidget(self.lin_xzerolineg, 26, 2, 1, 1)
        self.xaxis_grid.addWidget(self.lin_xzerolineb, 26, 3, 1, 1)
        self.xaxis_grid.addWidget(self.lin_xzerolinea, 26, 4, 1, 1)
        self.xaxis_grid.addWidget(self.btn_xzerolinec, 26, 5, 1, 1)
        self.xaxis_grid.addWidget(self.lbl_xside, 27, 0, 1, 1)
        self.xaxis_grid.addWidget(self.combo_xside, 27, 1, 1, 1)

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
        self.vbox1 = QVBoxLayout()
        self.vbox1.addWidget(self.general_group)
        self.vbox1.addWidget(self.title_group)
        self.vbox1.addWidget(self.xaxis_group)
        self.vbox1.addWidget(self.yaxis_group)
        self.vbox1.addStretch()
        scroll_aux = QWidget()
        scroll_aux.setLayout(self.vbox1)
        scroll = QScrollArea()
        scroll.setWidget(scroll_aux)
        scroll.setWidgetResizable(True)

        self.vbox2 = QVBoxLayout()
        self.vbox2.addLayout(self.hbox)
        self.vbox2.addWidget(scroll)

        centralw = QWidget()
        centralw.setLayout(self.vbox2)
        self.setCentralWidget(centralw)
        self.show()

        self.init_attributes()
        self.toggle_enable_fields()

        #self.general_group.toggle_button.click()
        #self.title_group.toggle_button.click()
        self.xaxis_group.toggle_button.click()
        #self.yaxis_group.toggle_button.click()

    def toggle_enable_fields(self):
        # General
        self.lin_laywidth.setEnabled(not self.chk_layautosize.isChecked())
        self.lin_layheight.setEnabled(not self.chk_layautosize.isChecked())

        # X axis
        self.lin_xtickangle.setEnabled(not self.chk_xtickangle.isChecked())
        self.lin_xlinewid.setEnabled(self.chk_xshowline.isChecked())
        self.btn_xlinec.setEnabled(self.chk_xshowline.isChecked())
        self.lin_xliner.setEnabled(self.chk_xshowline.isChecked())
        self.lin_xlineg.setEnabled(self.chk_xshowline.isChecked())
        self.lin_xlineb.setEnabled(self.chk_xshowline.isChecked())
        self.lin_xlinea.setEnabled(self.chk_xshowline.isChecked())
        self.lin_xgridwid.setEnabled(self.chk_xshowgrid.isChecked())
        self.btn_xgridc.setEnabled(self.chk_xshowgrid.isChecked())
        self.lin_xgridr.setEnabled(self.chk_xshowgrid.isChecked())
        self.lin_xgridg.setEnabled(self.chk_xshowgrid.isChecked())
        self.lin_xgridb.setEnabled(self.chk_xshowgrid.isChecked())
        self.lin_xgrida.setEnabled(self.chk_xshowgrid.isChecked())
        self.lin_xzerolinewid.setEnabled(self.chk_xzeroline.isChecked())
        self.btn_xzerolinec.setEnabled(self.chk_xzeroline.isChecked())
        self.lin_xzeroliner.setEnabled(self.chk_xzeroline.isChecked())
        self.lin_xzerolineg.setEnabled(self.chk_xzeroline.isChecked())
        self.lin_xzerolineb.setEnabled(self.chk_xzeroline.isChecked())
        self.lin_xzerolinea.setEnabled(self.chk_xzeroline.isChecked())

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
            elif target=='xaxis':
                self.lin_xr.setText(str(color.red()))
                self.lin_xg.setText(str(color.green()))
                self.lin_xb.setText(str(color.blue()))
            elif target=='xaxis_title':
                self.lin_xtitler.setText(str(color.red()))
                self.lin_xtitleg.setText(str(color.green()))
                self.lin_xtitleb.setText(str(color.blue()))
            elif target=='xaxis_tick':
                self.lin_xtickr.setText(str(color.red()))
                self.lin_xtickg.setText(str(color.green()))
                self.lin_xtickb.setText(str(color.blue()))
            elif target=='xaxis_line':
                self.lin_xliner.setText(str(color.red()))
                self.lin_xlineg.setText(str(color.green()))
                self.lin_xlineb.setText(str(color.blue()))
            elif target=='xaxis_grid':
                self.lin_xgridr.setText(str(color.red()))
                self.lin_xgridg.setText(str(color.green()))
                self.lin_xgridb.setText(str(color.blue()))
            elif target=='xaxis_zeroline':
                self.lin_xzeroliner.setText(str(color.red()))
                self.lin_xzerolineg.setText(str(color.green()))
                self.lin_xzerolineb.setText(str(color.blue()))

    def layout_update(self):
        """Reads fields and updates parent's layout"""
        changes = AutoDictionary()

        # General
        if str(self.combo_layhover.currentText()) == 'False':
            changes['hovermode'] = False
        else:
            changes['hovermode'] = str(self.combo_layhover.currentText())
        changes['autosize'] = self.chk_layautosize.isChecked()
        changes['width'] = int(self.lin_laywidth.text()) if self.lin_laywidth.isEnabled() else None
        changes['height'] = int(self.lin_layheight.text()) if self.lin_layheight.isEnabled() else None
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

        # X axis
        changes['xaxis']['visible'] = self.chk_xvisible.isChecked()
        r = str(self.lin_xr.text())
        g = str(self.lin_xg.text())
        b = str(self.lin_xb.text())
        a = str(self.lin_xa.text())
        changes['xaxis']['color'] = 'rgb('+r+','+g+','+b+','+a+')'
        #changes['xaxis']['title']['text'] = str(self.lin_xtitletext.text())
        changes['xaxis']['title']['font']['family'] = str(self.combo_xtitlefont.currentText())
        changes['xaxis']['title']['font']['size'] = int(self.lin_xtitlefont.text())
        r = str(self.lin_xtitler.text())
        g = str(self.lin_xtitleg.text())
        b = str(self.lin_xtitleb.text())
        a = str(self.lin_xtitlea.text())
        changes['xaxis']['title']['font']['color'] = 'rgb('+r+','+g+','+b+','+a+')'
        changes['xaxis']['type'] = str(self.combo_xtype.currentText())
        changes['xaxis']['autorange'] = self.chk_xautorange.isChecked()
        changes['xaxis']['nticks'] = int(self.lin_xnticks.text())
        changes['xaxis']['ticks'] = str(self.combo_xticks.currentText())
        changes['xaxis']['ticklen'] = int(self.lin_xticklen.text())
        changes['xaxis']['tickwidth'] = int(self.lin_xtickwid.text())
        r = str(self.lin_xtickr.text())
        g = str(self.lin_xtickg.text())
        b = str(self.lin_xtickb.text())
        a = str(self.lin_xticka.text())
        changes['xaxis']['tickcolor'] = 'rgb('+r+','+g+','+b+','+a+')'
        changes['xaxis']['showticklabels'] = self.chk_xshowticklabels.isChecked()
        changes['xaxis']['tickangle'] = None if self.chk_xtickangle.isChecked else int(self.lin_xtickangle.text())
        changes['xaxis']['tickprefix'] = str(self.lin_xtickprefix.text())
        changes['xaxis']['showtickprefix'] = str(self.combo_xshowtickprefix.currentText())
        changes['xaxis']['ticksuffix'] = str(self.lin_xticksufix.text())
        changes['xaxis']['showticksuffix'] = str(self.combo_xshowticksufix.currentText())
        changes['xaxis']['showexponent'] = str(self.combo_xshowexponent.currentText())
        changes['xaxis']['exponentformat'] = str(self.combo_xexponent.currentText())
        changes['xaxis']['tickformat'] = str(self.lin_xtickformat.text())
        changes['xaxis']['showline'] = self.chk_xshowline.isChecked()
        changes['xaxis']['linewidth'] = int(self.lin_xlinewid.text())
        r = str(self.lin_xliner.text())
        g = str(self.lin_xlineg.text())
        b = str(self.lin_xlineb.text())
        a = str(self.lin_xlinea.text())
        changes['xaxis']['linecolor'] = 'rgb('+r+','+g+','+b+','+a+')'
        changes['xaxis']['showgrid'] = self.chk_xshowgrid.isChecked()
        changes['xaxis']['gridwidth'] = int(self.lin_xgridwid.text())
        r = str(self.lin_xgridr.text())
        g = str(self.lin_xgridg.text())
        b = str(self.lin_xgridb.text())
        a = str(self.lin_xgrida.text())
        changes['xaxis']['gridcolor'] = 'rgb('+r+','+g+','+b+','+a+')'
        changes['xaxis']['zeroline'] = self.chk_xzeroline.isChecked()
        changes['xaxis']['zerolinewidth'] = int(self.lin_xzerolinewid.text())
        r = str(self.lin_xzeroliner.text())
        g = str(self.lin_xzerolineg.text())
        b = str(self.lin_xzerolineb.text())
        a = str(self.lin_xzerolinea.text())
        changes['xaxis']['zerolinecolor'] = 'rgb('+r+','+g+','+b+','+a+')'
        changes['xaxis']['side'] = str(self.combo_xside.currentText())

        # Run layout update
        self.parent.layout_update(changes=changes)

    def init_attributes(self):
        pass
