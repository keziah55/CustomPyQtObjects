#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QStackedWidget that stores references to its pages in a dict.
"""
from qtpy.QtWidgets import QStackedWidget
from uuid import uuid4

class StackedWidget(QStackedWidget):
    """ QStackedWidget that stores references to its pages in a dict. 
    
        Also can pass dict of `pages` to initialise the stack.
    """
    def __init__(self, *args, pages={}, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._widgetDict = {}
        for key, widget in pages.items():
            self.addWidget(widget, key)
            
    def __getitem__(self, key):
        """ Get widget identified by `key` """
        widget = self._widgetDict.get(key, None)
        if widget is not None:
            return widget
        else:
            raise KeyError(f"StackedWidget has no widget '{key}'")
            
    @property
    def widgetDict(self):
        """ Return dictionary of keys and widgets """
        return self._widgetDict
    
    @property
    def widgets(self):
        """ Return list of all widgets """
        return [self.widget(idx) for idx in range(self.count())]
            
    def addWidget(self, widget, key=None) -> int:
        """ Add `widget` to the stack, associated with key `key`. 
        
            If `key` not provided a uuid will be generated.
        """
        if key is None:
            key = uuid4()
        if key in self._widgetDict:
            raise KeyError(f"Key '{key}' already present in StackedWidget")
        self._widgetDict[key] = widget
        return super().addWidget(widget)
    
    def insertWidget(self, index, widget, key=None) -> int:
        """ Insert `widget` to the stack, associated with key `key`, at position `index`
        
            If `key` not provided a uuid will be generated.
        """
        if key is None:
            key = uuid4()
        if key in self._widgetDict:
            raise KeyError(f"Key '{key}' already present in StackedWidget")
        self._widgetDict[key] = widget
        return super().insertWidget(index, widget)
    
    def removeWidget(self, widget):
        """ Remove `widget` from stack. 
        
            `widget` can be a QWidget instance or a key.
        """
        if widget in self._widgetDict:
            widget = self._widgetDict[widget]
        super().removeWidget(widget)
        del self._widgetDict[widget]
        
    def keyOf(self, widget):
        """ Return key associated with `widget`. """
        for key, value in self._widgetDict.items():
            if value == widget:
                return key
        return None
    
    def setCurrentKey(self, key):
        """ Set current widget to that identified by `key` """
        self.setCurrentWidget(self._widgetDict[key])