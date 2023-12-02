#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QTableWidget with convenience methods for adding a whole row at a time etc.
"""
from qtpy.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from ..gui import makeBrush

class TableWidget(QTableWidget):
    
    def __init__(self, horizontalHeader=None, verticalHeader=None, resizeMode=None):
        super().__init__()
        
        if horizontalHeader is not None:
            self.setColumnCount(len(horizontalHeader))
            self.setHorizontalHeaderLabels(horizontalHeader)
            
        if verticalHeader is not None:
            self.setVerticalHeaderLabels(verticalHeader)
            
        if resizeMode is not None:
            self.setResizeMode(resizeMode)
            
        self._header = horizontalHeader
            
    @property
    def columnCount(self):
        return super().columnCount()
    
    @property
    def rowCount(self):
        return super().rowCount()
    
    @property
    def header(self):
        return self._header
    
    def clearTable(self):
        for idx in reversed(range(self.rowCount)):
            self.removeRow(idx)
    
    def _parseRowKwargs(self, **kwargs):
        names = ['background', 'checkState', 'data', 'flags', 'font', 'foreground',
                 'icon', 'selected', 'sizeHint', 'statusTip', 'textAlignment',
                 'toolTip', 'whatsThis']
        d = {}
        for key in names:
            if key not in kwargs:
                continue
            value = kwargs[key]
            if key in ['background', 'foreground']:
                value = makeBrush(value)
            d[key] = self._makeRowArgs(value)
        return d
        
    def _makeRowArgs(self, value):
        """ 
        If `value` is not a list or tuple, create list of `value` repeated `columnCount` times 
        
        If `value` is a list or tuple of values, it will be returned.
        """
        if not isinstance(value, (list, tuple)):
            value = [value] * self.columnCount
        if len(value) != self.columnCount:
            msg = f"List of {self.columnCount} values needed, got {value}"
            raise ValueError(msg)
        return value
    
    def addRow(self, row:list, **kwargs):
        """ 
        Add row to table 
        
        Parameters
        ----------
        row : list, tuple
            Sequence of strings or (icon,string) pairs from which to construct
            [QTableWidgetItems](https://doc.qt.io/qt-6/qtablewidgetitem.html)
        kwargs 
            Any QTableWidgetItem setter can be passed here, e.g. `toolTip='this is the tool tip'`
            will call `setToolTip('this is the tool tip')` after creating the item.
            `background` and `foreground` can be passed with a 
            [QBrush](https://doc.qt.io/qt-6/qbrush.html), [QColor](https://doc.qt.io/qt-6/qcolor.html) or
            any valid QColor arg.
        """
        kwargs = self._parseRowKwargs(**kwargs)
        rowNum = self.rowCount
        self.insertRow(rowNum)
        for col, arg in enumerate(row):
            if isinstance(arg, (tuple,list)):
                item = QTableWidgetItem(*arg)
            else:
                item = QTableWidgetItem(arg)
            for name, values in kwargs.items():
                # call setters with corresponding value
                name = name[0].upper() + name[1:]
                func = getattr(item, f"set{name}")
                func(values[col])
                
            self.setItem(rowNum, col, item)
            
    def updateRow(self, idx:int, row:list, **kwargs):
        """
        Update data in row number `idx`
        
        Parameters
        ----------
        idx : int
            Index of row to update
        row : list, tuple
            Sequence of strings or (icon,string) pairs from which to construct
            [QTableWidgetItems](https://doc.qt.io/qt-6/qtablewidgetitem.html)
        kwargs 
            Any QTableWidgetItem setter can be passed here, e.g. `toolTip='this is the tool tip'`
            will call `setToolTip('this is the tool tip')` on the item.
            `background` and `foreground` can be passed with a 
            [QBrush](https://doc.qt.io/qt-6/qbrush.html), [QColor](https://doc.qt.io/qt-6/qcolor.html) or
            any valid QColor arg.
        """
        for col in self.columnCount:
            item = self.item(idx, col)
            # update text and icon
            if  isinstance(row[col], (tuple,list)):
                icon, text = row[col]
                item.setIcon(icon)
            else:
                text = row[col]
            item.setText(text)
            # update any other properties
            for name, values in kwargs.items():
                setattr(item, f"set{name.title()}", values[col])
    
    def rowData(self, idx, returnType='dict'): 
        row = [self.item(idx, col).text() for col in range(self.colCount)]
        if returnType == 'dict':
            if len(self.header) != len(row):
                msg = "Cannot return row data as dict when horizontal header items are None"
                raise Exception(msg)
            row = dict(zip(self.header, row))
        return row

    def columnData(self, name): 
        idx = self.header.index(name)
        column = [self.item(row, idx) for row in range(self.rowCount)]
        return column

    def rowWhere(self, columnName, value, returnType='dict'): 
        values = []
        col = self.header.index(columnName)
        for row in range(self.rowCount):
            if self.item(row, col).text() == value:
                values = [self.item(row, idx).text() for idx in range(self.colCount)]
                break
        if returnType == 'dict':
            if len(self.header) != len(values):
                msg = "Cannot return row data as dict when horizontal header items or values are None"
                raise ValueError(msg)
            row = dict(zip(self.header, values))
        return values
    
    def setResizeMode(self, mode):
        """ 
        Set resize mode for horizontal header 
        
        Parameters
        ----------
        mode : {list, QHeaderView.ResizeMode, str}
            Resize mode. If a single value is given it will be applied to all. 
            Otherwise, pass a list. The values can be [QHeaderView.ResizeMode](https://doc.qt.io/qt-6/qheaderview.html#ResizeMode-enum)
            or corresponding string 'Interactive', 'Fixed', 'Stretch', 'ResizeToContents'
            (strings are not case sensitive).
        """
        error_msg = ("TableWidget resizeMode should be 'Interactive', 'Fixed', "
                     f"'Stretch' or 'ResizeToContents', not '{mode}'")
        
        modes = {'interactive':QHeaderView.Interactive, 
                 'fixed':QHeaderView.Fixed, 
                 'stretch':QHeaderView.Stretch, 
                 'resizetocontents':QHeaderView.ResizeToContents}
        if isinstance(mode, str):
            mode = modes.get(mode.lower(), None)
            if mode is None:
                raise ValueError(error_msg)
        if isinstance(mode, list): 
            for idx, m in enumerate(mode):
                if isinstance(m, str):
                    mode[idx] = modes.get(m.lower(), None)
                if mode[idx] not in modes.values():
                    raise ValueError(error_msg)
            
        mode = self._makeRowArgs(mode)
        for idx, m in enumerate(mode):
            self.horizontalHeader().setSectionResizeMode(idx, m)
