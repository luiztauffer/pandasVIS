from PySide2 import QtCore, QtGui
from PySide2.QtWidgets import QTreeWidget, QMenu


class QTreeCustomPrimary(QTreeWidget):
    def __init__(self, parent):
        QTreeWidget.__init__(self, parent)
        self.parent = parent
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.contextMenuEvent)

    def contextMenuEvent(self, event):
        """Tests if click was over a valid item."""
        index = self.indexAt(event)
        if index.isValid():
            item = self.itemAt(event)
            name = item.text(0)   # the text of the node
            self.contextMenu1(name=name, event=event)
        else:
            name = None

    def contextMenu1(self, name, event):
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

        self.menu.popup(QtGui.QCursor.pos())
        action = self.menu.exec_(self.mapToGlobal(event))

        if action is not None:
            if action.text() == 'Summary':
                print('')
            if action.text() == 'Set as Index':
                pass # self.parent.df.
            if action.text() == 'Transform':
                print('')
            if action.text() == 'Group-by':
                print('')
            if action.text() == 'Move to Secondary':
                move_to_secondary(parent=self.parent, name=name)
            if action.text() == 'Delete':
                self.parent.df.drop(name, axis=1, inplace=True)
                self.parent.primary_names = self.parent.df.keys().tolist()
                self.parent.console.push_vars({'df': self.parent.df})
                self.parent.init_trees()


class QTreeCustomSecondary(QTreeWidget):
    def __init__(self, parent):
        QTreeWidget.__init__(self, parent)
        self.parent = parent
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.contextMenuEvent)

    def contextMenuEvent(self, event):
        """Tests if click was over a valid item."""
        index = self.indexAt(event)
        if index.isValid():
            item = self.itemAt(event)
            name = item.text(0)   # the text of the node
            self.contextMenu1(name=name, event=event)
        else:
            name = None

    def contextMenu1(self, name, event):
        self.menu = QMenu()
        var_name = self.menu.addAction(name)
        f = QtGui.QFont()
        f.setBold(True)
        var_name.setFont(f)
        self.menu.addSeparator()
        act_summary = self.menu.addAction('Summary')
        act_transform = self.menu.addAction('Transform')
        act_primary = self.menu.addAction('Move to Primary')
        act_delete = self.menu.addAction('Delete')

        self.menu.popup(QtGui.QCursor.pos())
        action = self.menu.exec_(self.mapToGlobal(event))

        if action is not None:
            if action.text() == 'Summary':
                print('')
            if action.text() == 'Transform':
                print('')
            if action.text() == 'Move to Primary':
                move_to_primary(parent=self.parent, name=name)
            if action.text() == 'Delete':
                del self.parent.secondary_vars[name]
                self.parent.secondary_names = list(self.parent.secondary_vars.keys())
                self.parent.console.push_vars({'secondary_vars': self.parent.secondary_vars})
                self.parent.init_trees()


def move_to_secondary(parent, name):
    """Moves a variable from Primary to Secondary list of variables. Removes it from df."""
    parent.secondary_vars[name] = parent.df[name]
    parent.secondary_names = list(parent.secondary_vars.keys())
    parent.df.drop(name, axis=1, inplace=True)
    parent.primary_names = parent.df.keys().tolist()
    # Update df and secondary_vars on console
    parent.console.push_vars({'df': parent.df})
    parent.console.push_vars({'secondary_vars': parent.secondary_vars})
    # Update trees
    parent.init_trees()


def move_to_primary(parent, name):
    """Moves a variable from Secondary to Primary list of variables. Adds it to df."""
    if parent.df.shape[0] == len(parent.secondary_vars[name]):
        parent.df[name] = parent.secondary_vars[name]
        parent.primary_names = parent.df.keys().tolist()
        del parent.secondary_vars[name]
        parent.secondary_names = list(parent.secondary_vars.keys())
        # Update df and secondary_vars on console
        parent.console.push_vars({'df': parent.df})
        parent.console.push_vars({'secondary_vars': parent.secondary_vars})
        # Update trees
        parent.init_trees()
    else:
        # TO-DO needs to raise a popup warning in the future
        print('Variable of different length from df')
