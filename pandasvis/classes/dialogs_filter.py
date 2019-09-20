from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from threading import Event, Thread
import numpy as np
import pandas as pd
import os

# Path where UI files are
ui_path = os.path.join(os.path.dirname(__file__), '..', 'ui')


# Filter variables dialog ------------------------------------------------------
Ui_FilterVars, _ = uic.loadUiType(os.path.join(ui_path, "filter_variables.ui"))
class FilterVariablesDialog(QDialog, Ui_FilterVars):
    def __init__(self, parent, df):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Add filters')
        self.parent = parent
        self.df = df
        self.value = -1
        self.all_operations = []
        self.group_by = None

        self.comboBox_0.activated.connect(lambda: self.update_current_condition('cb0'))
        self.comboBox_1.activated.connect(lambda: self.update_current_condition(None))
        self.comboBox_2.activated.connect(lambda: self.update_current_condition(None))
        self.comboBox_3.activated.connect(lambda: self.update_current_condition('rb1'))
        self.radioButton_1.clicked.connect(lambda: self.update_current_condition('rb1'))
        self.radioButton_2.clicked.connect(lambda: self.update_current_condition('rb2'))
        self.lineEdit_1.textChanged.connect(lambda: self.update_current_condition('rb2'))

        self.pushButton_1.clicked.connect(self.add_condition)
        self.pushButton_2.clicked.connect(self.clear_conditions)
        self.pushButton_accept.clicked.connect(lambda: self.exit(val=1))
        self.pushButton_cancel.clicked.connect(lambda: self.exit(val=-1))

        self.init_dropdowns()
        self.exec_()

    def init_dropdowns(self):
        operations = ['==', '!=', '<', '>']
        for op in operations:
            self.comboBox_2.addItem(op)
        vars = list(self.df.columns)
        self.comboBox_0.addItem('None')
        for var in vars:
            if self.df[var].dtype.name in ['object', 'bool', 'category']:
                self.comboBox_0.addItem(var)
            self.comboBox_1.addItem(var)
            self.comboBox_3.addItem(var)

    def update_current_condition(self, src=None):
        # Check source
        if src == 'cb0':
            if self.comboBox_0.currentText() != 'None':
                self.txt1 = self.comboBox_0.currentText()
                self.txt2 = 'group by'
                self.txt3 = None
                self.textEdit_1.setText('group by ' + self.txt1)
            return
        if src == 'rb1':
            self.radioButton_1.setChecked(True)
        elif src == 'rb2':
            self.radioButton_2.setChecked(True)
        # Operand 1
        self.txt1 = self.comboBox_1.currentText()
        # Operation
        self.txt2 = self.comboBox_2.currentText()
        # Operand 2
        if self.radioButton_1.isChecked():
            self.txt3 = self.comboBox_3.currentText()
        else:
            self.txt3 = self.lineEdit_1.text()
        # Write text for current chosen condition
        self.textEdit_1.setText(self.txt1 + ' ' + self.txt2 + ' ' + self.txt3)

    def add_condition(self):
        # Add to list of operations
        aux = {}
        aux['operand_1'] = self.txt1
        aux['operation'] = self.txt2
        aux['operand_2'] = self.txt3
        aux['type_1'] = 'variable'
        if self.txt2 == 'group by':
            aux['type_2'] = None
        else:
            if self.radioButton_1.isChecked():
                aux['type_2'] = 'variable'
            else:
                aux['type_2'] = 'other'
        self.all_operations.append(aux)
        # Add text
        curr_cond = self.textEdit_1.toPlainText()
        curr_all = self.textEdit_2.toPlainText()
        if curr_all == '':
            self.textEdit_2.setText(curr_cond)
        else:
            self.textEdit_2.setText('('+curr_all+') AND ('+curr_cond+')')

    def clear_conditions(self):
        self.textEdit_2.setText('')
        self.all_operations = []

    def parse_conditions(self):
        nObs = self.df.shape[0]
        mask = np.full(nObs, True)
        for op in self.all_operations:
            print(op)
            # Test type of variable 1
            if op['type_1'] == 'variable':
                op1 = self.df[op['operand_1']]
            else:
                op1 = op['operand_1']

            # Test type of variable 2
            if op['type_2'] == 'variable':
                op2 = self.df[op['operand_2']]
            elif op['type_2'] == 'str':
                op2 = op['operand_2']
            elif op['type_2'] is not None:
                op2 = float(op['operand_2'])

            # Possible operations: ['group by', '==', '!=', '<', '>']
            if op['operation'] == 'group by':
                self.group_by = op['operand_1']
            elif op['operation'] == '==':
                aux = (op1 == op2).to_numpy()
                mask = mask*aux
            elif op['operation'] == '!=':
                aux = (op1 != op2).to_numpy()
                mask = mask*aux
            elif op['operation'] == '<':
                aux = (op1 < op2).to_numpy()
                mask = mask*aux
            elif op['operation'] == '>':
                aux = (op1 > op2).to_numpy()
                mask = mask*aux
        self.df = self.df[mask]

    def exit(self, val=-1):
        self.value = val
        if val == 1:
            self.parse_conditions()
        self.accept()
