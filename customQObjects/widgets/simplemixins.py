#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Some very simple mixins
"""
from qtpy.QtCore import Signal

class ClickMixin(object):
    """ Emit a `clicked` signal in :meth:`mouseReleaseEvent` """
    
    clicked = Signal()
    """ Signal emitted in :meth:`mouseReleaseEvent` """
    
    def mouseReleaseEvent(self, event):
        """ Emit :attr:`clicked` and call `super().mouseReleaseEvent` """
        self.clicked.emit()
        return super().mouseReleaseEvent(event)