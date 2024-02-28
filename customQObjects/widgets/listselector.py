#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple widget to show a list of values and highlight the current one.
"""
from qtpy.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QFrame
from qtpy.QtCore import Qt

class StyledLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._css_style = ""
        self._plain_text = ""
        
    def set_css_style(self, style=None):
        if style is None:
            self._css_style = ""
        else:
            self._css_style = f' style="{style}"'
        
    def set_text(self, text):
        self._plain_text = text
        html = self._make_html()
        super().setText(html)
        
    def setText(self, text):
        return self.set_text(text)
    
    def text(self):
        return self._plain_text
        
    def _make_html(self):
        s = f'<p{self._css_style}>{self._plain_text}</p>'
        return s

class ListSelector(QFrame):
    """
    Widget showing a list of strings, with the current one highlighted.
    
    Parameters
    ----------
    values : list[str]
        List of strings to show
    orientation : {'vertical', 'horizontal'}
        Orientation for list of widgets.
    style : str, optional
        Html style to use for each label.
    """
    def __init__(self, *args, values:list[str], orientation:str="vertical", style=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        valid = ["vertical", "horizontal"]
        if orientation not in valid:
            msg = f"Invalid orientation '{orientation}'. "
            msg += "Valid orientations are 'vertical' or 'horizontal'"
            raise ValueError(msg)
            
        self._current_idx = 0
        
        self.labels = []
        
        self.layout = QVBoxLayout() if orientation == "vertical" else QHBoxLayout()
        
        for value in values:
            label = StyledLabel()
            label.set_css_style(style)
            label.set_text(value)
            
            label.setFrameShape(QFrame.NoFrame)
            label.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(label)
            self.labels.append(label)
        
        self.setLayout(self.layout)
        
        self.setFrameShape(QFrame.Box)
        self.set_current_index(0)
        
    @property
    def current_index(self):
        """ Index of currently highlighted label. """
        return self._current_idx
    
    @current_index.setter
    def current_index(self, idx):
        self.set_current_index(idx)
        
    @property
    def current_text(self):
        """ Text of currently highlighted label. """
        return self.labels[self._current_idx].text()
    
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