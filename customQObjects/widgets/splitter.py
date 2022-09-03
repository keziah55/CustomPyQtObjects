from qtpy.QtWidgets import QSplitter, QWidget
from qtpy.QtCore import Qt

class Splitter(QSplitter):
    """ QSplitter with :meth:`addLayout` method """
    
    def addLayout(self, layout):
        """ Add `layout` to splitter by creating a container widget for it """
        container = QWidget()
        container.setLayout(layout)
        self.addWidget(container)
        
class VSplitter(Splitter):
    """ :class:`Splitter` with vertical orientation """
    def __init__(self, parent=None):
        super().__init__(Qt.Vertical, parent=parent)
        
class HSplitter(Splitter):
    """ :class:`Splitter` with horizontal orientation """
    def __init__(self, parent=None):
        super().__init__(Qt.Horizontal, parent=parent)
    