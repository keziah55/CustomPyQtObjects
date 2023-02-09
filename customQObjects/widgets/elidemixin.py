"""
:class:`ElideMixin` automatically elides text.

:class:`ElideLabel` is a QLabel that uses the :class:`ElideMixin`
"""

from qtpy.QtWidgets import QLabel
from qtpy.QtCore import Qt
from qtpy.QtGui import QFontMetrics

class ElideMixin(object):
    """ 
    Mixin providing functionality to automatically elide text 
    
    Parameters
    ----------
    elideMode : {'middle', 'left', 'right', 'None', Qt.TextElideMode}
        Text elide mode, either as string or [Qt.TextElideMode](https://doc.qt.io/qt-6/qt.html#TextElideMode-enum>)
    widthAdjust : int, optional
        If provided, this value will be added to the widget's width when 
        calling [QFontMetrics.elidedText](https://doc.qt.io/qt-6/qfontmetrics.html#elidedText)
    """
    elideModes = {'left':Qt.ElideLeft, 'middle':Qt.ElideMiddle, 'right':Qt.ElideRight,
                  'none':Qt.ElideNone}
    
    def __init__(self, *args, elideMode='middle', widthAdjust=0, **kwargs):
        self._fullText = ""
        self._widthAdjust = widthAdjust
        self._elideMode = self._validateMode(elideMode)
        
        super().__init__(*args, **kwargs)
        
    @property
    def fullText(self):
        """ Un-elided text """
        return self._fullText
        
    @property
    def elideMode(self):
        """ Current elide mode """
        return self._elideMode
        
    @elideMode.setter
    def elideMode(self, mode):
        """ Set elide mode and update text """
        self._elideMode = self._validateMode(mode)
        self._resetText()
        
    @property
    def widthAdjust(self):
        """ Current width adjust """
        return self._widthAdjust
    
    @widthAdjust.setter 
    def widthAdjust(self, value):
        """ Set width adjust and update text """
        self._widthAdjust = value
        self._resetText()
        
    def _validateMode(self, mode):
        """ Return requested Qt.TextElideMode """
        if mode is None:
            mode = 'none'
        if isinstance(mode, str):
            mode = mode.lower()
            if mode not in self.elideModes:
                raise ValueError(f"'{mode}' not valid elide mode")
            else:
                mode = self.elideModes[mode]
        else:
            if mode not in self.elideModes.values():
                raise ValueError(f"'{mode}' not valid elide mode")
        return mode
    
    def setText(self, text):
        """ Elide `text` and set it """
        self._fullText = text
        metrics = QFontMetrics(self.font())
        elided = metrics.elidedText(text, self.elideMode, self.width()+self.widthAdjust)
        super().setText(elided)
        self.setToolTip(self._fullText)
        
    def _resetText(self):
        """ Reset text from :attr:`fullText` """
        self.setText(self._fullText)
        
    def resizeEvent(self, event):
        """ Override resizeEvent to update text """
        self._resetText()
        
class ElideLabel(ElideMixin, QLabel):
    """ [QLabel](https://doc.qt.io/qt-5/qlabel.html) that automatically elides its text.
    
        See [ElideMixin][customQObjects.widgets.ElideMixin] for additional args and kwargs.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(args) == 1:
            self.setText(args[0])
