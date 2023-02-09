#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QTableWidget with convenience methods for adding a whole row at a time etc.
"""
from qtpy.QtWidgets import QTableWidget, QTableWidgetItem

class TableWidget(QTableWidget):
    
    def __init__(self, horizontalHeader=None, verticalHeader=None, resizeMode=None):
        super().__init__()
        
        if horizontalHeader is not None:
            self.setHorizontalHeaderLabels(self.header)
        if verticalHeader is not None:
            self.setVerticalHeaderLabels(self.header)
            
        if resizeMode is not None:
            if not isinstance(resizeMode, (list, tuple)):
                if horizontalHeader is None:
                    msg = "Cannot assign table section resize mode with unknown number of columns"
                    raise ValueError(msg)
                resizeMode = [resizeMode] * len(horizontalHeader)
            headerView = self.horizontalHeader()
            for idx, mode in enumerate(resizeMode):
                headerView.setSectionResizeMode(idx, mode)
    
    def addRow(self, row, **kwargs):
        pass
    
    def updateRow(self, idx, row, **kwargs):
        pass
    
    def rowData(self, idx): 
        pass

    def columnData(self, name): 
        pass

    def rowWhere(self, columnName, value, returnType='dict'): 
        pass