from qtpy.QtWidgets import QSplitter, QWidget, QLayout
from qtpy.QtCore import Qt


class Splitter(QSplitter):
    """
    [QSplitter](https://doc.qt.io/qt-6/qsplitter.html) with
    [addLayout][customQObjects.widgets.Splitter.addLayout] method

    See Also
    --------
    [VSplitter][customQObjects.widgets.VSplitter]

    [HSplitter][customQObjects.widgets.HSplitter]
    """

    def addLayout(self, layout: QLayout):
        """Add `layout` to splitter by creating a container widget for it"""
        container = QWidget()
        container.setLayout(layout)
        self.addWidget(container)

    def setStretchFactors(self, stretch: list[int]):
        """Set multiple stretch factors from list"""
        for idx, sf in enumerate(stretch):
            self.setStretchFactor(idx, sf)


class VSplitter(Splitter):
    """[Splitter][customQObjects.widgets.Splitter] with vertical orientation"""

    def __init__(self, parent=None):
        super().__init__(Qt.Vertical, parent=parent)


class HSplitter(Splitter):
    """[Splitter][customQObjects.widgets.Splitter] with horizontal orientation"""

    def __init__(self, parent=None):
        super().__init__(Qt.Horizontal, parent=parent)
