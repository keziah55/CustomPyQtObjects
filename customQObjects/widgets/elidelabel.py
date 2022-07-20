from qtpy.QtWidgets import QLabel
from qtpy.QtCore import Qt
from qtpy.QtGui import QFontMetrics

class ElideMixin(object):
    elideModes = {'left':Qt.ElideLeft, 'middle':Qt.ElideMiddle, 'right':Qt.ElideRight,
                  'none':Qt.ElideNone}
    
    def __init__(self, *args, elideMode='middle', widthAdjust=0, **kwargs):
        self._fullText = ""
        super().__init__(*args, **kwargs)
        self.elideMode = elideMode
        self.widthAdjust = widthAdjust
        
    @property
    def fullText(self):
        return self._fullText
        
    @property
    def elideMode(self):
        return self._elideMode
        
    @elideMode.setter
    def elideMode(self, mode):
        self._elideMode = self._validateMode(mode)
        self._resetText()
        
    @property
    def widthAdjust(self):
        return self._widthAdjust
    
    @widthAdjust.setter 
    def widthAdjust(self, value):
        self._widthAdjust = value
        
    def _validateMode(self, mode):
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
        self._fullText = text
        metrics = QFontMetrics(self.font())
        elided = metrics.elidedText(text, self.elideMode, self.width()-self.widthAdjust)
        super().setText(elided)
        self.setToolTip(self._fullText)
        
    def _resetText(self):
        self.setText(self._fullText)
        
    def resizeEvent(self, event):
        self._resetText()
        
class ElideLabel(ElideMixin, QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(args) == 1:
            self.setText(args[0])
        
            
    