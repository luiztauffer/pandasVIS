from PyQt5 import QtCore, QtGui, Qt
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QMenu

class QTreeCustomPrimary(QTreeWidget):
    def __init__(self, parent=None):
        QTreeWidget.__init__(self, parent)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.contextMenuEvent)

    def contextMenuEvent(self, event):
        """Tests if click was over a valid item."""
        index = self.indexAt(event)
        if index.isValid():
            item = self.itemAt(event)
            name = item.text(0)  #The text of the node
            self.contextMenu1(name)
        else:
            name = None

    def contextMenu1(self, name):
        self.menu = QMenu()
        var_name = self.menu.addAction(name)
        f = QtGui.QFont()
        f.setBold(True)
        var_name.setFont(f)
        self.menu.addSeparator()
        act_summary = self.menu.addAction('Summary')
        act_index = self.menu.addAction('Set as Index')
        act_transform = self.menu.addAction('Transform')
        act_groupby = self.menu.addAction('Group-by')
        act_secondary = self.menu.addAction('Move to Secondary')
        act_delete = self.menu.addAction('Delete')
        #action = self.menu.exec_(self.mapToGlobal(event.pos()))
        self.menu.popup(QtGui.QCursor.pos())
