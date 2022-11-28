from qtpy.QtWidgets import (QGroupBox, QLayout, QHBoxLayout, QVBoxLayout, 
                            QGridLayout, QFormLayout)

class GroupBox(QGroupBox):
    """ `QGroupBox <https://doc.qt.io/qt-5/qgroupbox.html>`_ with a layout automatically set.
    
        Parameters
        ----------
        layout : {"vbox", "hbox", "grid", "form", QLayout}
            Type of layout to create. If given a QLayout instance, that will be
            used. Default is "vbox", i.e. QVBoxLayout.
        args 
            Args to pass to QGroupBox constructor
        kwargs 
            Kwargs to pass to QGroupBox constructor
    """
    def __init__(self, *args, layout="vbox", **kwargs):
        super().__init__(*args, **kwargs)
        
        layouts = {"vbox":QVBoxLayout, "hbox":QHBoxLayout, "grid":QGridLayout,
                   "form":QFormLayout}
        if isinstance(layout, str):
            if layout not in layout:
                valid = "'{}', '{}' or '{}'".format(*layouts.keys())
                msg = f"GroupBox direction should be {valid} or a QLayout instance, not '{layout}'"
                raise ValueError(msg)
            layoutObj = layouts[layout]
            self.layout = layoutObj()
        elif isinstance(layout, QLayout):
            self.layout = layout
        else:
            msg = f"GroupBox direction should be {valid} or a QLayout instance, not '{layout}'"
            raise ValueError(msg)
        self.setLayout(self.layout)
        
    def addWidget(self, *args, **kwargs):
        """ Add a widget to the internal layout. """
        return self.layout.addWidget(*args, **kwargs)
        
    def addLayout(self, *args, **kwargs):
        """ Add a layout to the internal layout. """
        return self.layout.addLayout(*args, **kwargs)

    def addRow(self, *args, **kwargs):
        """ Add row to a form layout """
        if not isinstance(self.layout, QFormLayout):
            raise RuntimeError(f"'addRow' method only exists for QFormLayouts, not {self.layout.__class__}")
        return self.layout.addRow(*args, **kwargs)