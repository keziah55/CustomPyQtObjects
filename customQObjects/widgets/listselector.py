#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple widget to show a list of values and highlight the current one.
"""
from qtpy.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame

class ListSelector(QWidget):
    """
    Widget showing a list of strings, with the current one highlighted.
    """
    def __init__(self, *args, values:list[str], orientation:str="vertical", **kwargs):
        super().__init__(*args, **kwargs)
        
        valid = ["vertical", "horizontal"]
        if orientation not in valid:
            msg = f"Invalid orientation '{orientation}'. "
            msg += "Valid orientations are 'vertical' or 'horizontal'"
            raise ValueError(msg)
            
        self._current_idx = 0
        
        self.labels = [QLabel(value) for value in values]
        
        self.layout = QVBoxLayout() if orientation == "vertical" else QHBoxLayout()
        
        for label in self.labels:
            label.setFrameShape(QFrame.NoFrame)
            self.layout.addWidget(label)
        
        self.setLayout(self.layout)
        
    @property
    def current_index(self):
        """ Index of currently highlighted label. """
        return self._current_index
    
    @current_index.setter
    def current_index(self, idx):
        self.set_current_index(idx)
        
    @property
    def current_text(self):
        """ Text of currently highlighted label. """
        return self._labels[self._current_idx].text()
    
    @current_text.setter
    def current_text(self, text):
        self.set_current_text(text)
        
    def set_current_text(self, text):
        """ 
        Set current label by `text`. 
        
        Raise ValueError if no label with `text` is found.
        """
        for idx, label in enumerate(self._labels):
            if label.text() == text:
                self.set_current_index(idx)
        
        msg = f"No label with text '{text}'"
        raise ValueError(msg)
        
    def set_current_index(self, idx):
        """ Highlight label at index `idx`. """
        self.labels[self._current_idx].setFrameShape(QFrame.NoFrame)
        self._current_idx = idx
        self.labels[self._current_idx].setFrameShape(QFrame.Box)
        
    def next(self):
        """ Highlight next label, looping back to beginning if at end. """
        if self.current_index == len(self.labels)-1:
            self.current_index = 0
        else:
            self.current_index += 1
            
    def previous(self):
        """ Highlight previous label, looping to end if at beginning. """
        if self.current_index == 0:
            self.current_index = len(self.labels)-1
        else:
            self.current_index -= 1