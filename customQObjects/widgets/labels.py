#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" A few simple `QLabel <https://doc.qt.io/qt-5/qlabel.html>`_ subclasses """

from qtpy.QtWidgets import QLabel
from qtpy.QtCore import Signal
from .elidemixin import ElideMixin

class ClickLabel(QLabel):
    """ `QLabel <https://doc.qt.io/qt-5/qlabel.html>`_ that emits a `clicked` signal """
    
    clicked = Signal()
    """ Signal emitted in :meth:`mouseReleaseEvent` """
    
    def mouseReleaseEvent(self, event):
        """ Emit :attr:`clicked` and call `super().mouseReleaseEvent` """
        self.clicked.emit()
        return super().mouseReleaseEvent(event)
    
class ElideLabel(ElideMixin, ClickLabel):
    """ `QLabel <https://doc.qt.io/qt-5/qlabel.html>`_ that automatically elides its text.
    
        See :class:`ElideMixin` for additional args and kwargs.
        
        Also emits :attr:`clicked` signal. See :class:`ClickLabel`.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(args) == 1:
            self.setText(args[0])
