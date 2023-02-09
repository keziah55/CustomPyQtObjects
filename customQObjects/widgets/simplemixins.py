#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Some very simple mixins
"""
from qtpy.QtCore import Signal

class ClickMixin(object):
    """ Emit a `clicked` signal in [mouseReleaseEvent][customQObjects.widgets.simplemixins.ClickMixin.mouseReleaseEvent] """
    
    clicked = Signal()
    """ Signal emitted in [mouseReleaseEvent][customQObjects.widgets.simplemixins.ClickMixin.mouseReleaseEvent] """
    
    def mouseReleaseEvent(self, event):
        """ Emit [clicked][customQObjects.widgets.simplemixins.ClickMixin.clicked] signal and call `super().mouseReleaseEvent` """
        self.clicked.emit()
        return super().mouseReleaseEvent(event)