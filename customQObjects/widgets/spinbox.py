"""
QSpinBox and QDoubleSpinBox subclasses that allow min and max to be essentially unset.
"""
from qtpy.QtWidgets import QSpinBox, QDoubleSpinBox
import sys

class SpinBox(QSpinBox):
    """ 
    [QSpinBox](https://doc.qt.io/qt-6/qspinbox.html) that allows min and max to be essentially unset. 
    
    See Also
    --------
    [DoubleSpinBox][customQObjects.widgets.DoubleSpinBox]
    """
    def setMinimum(self, value:int=None):
        """ Set minimum value. If `None`, there will be no minimum """
        if value is None:
            value = -2147483648
        return super().setMinimum(value)
    
    def setMaximum(self, value:int=None):
        """ Set maximum value. If `None`, there will be no maximum """
        if value is None:
            value = 2147483647
        return super().setMaximum(value)
    
    def setRange(self, minimum:int=None, maximum:int=None):
        """ Set minimum and/or maximum """
        self.setMinimum(minimum)
        self.setMaximum(maximum)
    
class DoubleSpinBox(QDoubleSpinBox):
    """ 
    [QDoubleSpinBox](https://doc.qt.io/qt-6/qsdoublepinbox.html) that allows min and max to be essentially unset. 
    
    See Also
    --------
    [SpinBox][customQObjects.widgets.SpinBox]
    """
    def setMinimum(self, value:float=None):
        """ Set minimum value. If `None`, there will be no minimum """
        if value is None:
            value = -sys.float_info.max
        return super().setMinimum(value)
    
    def setMaximum(self, value:float=None):
        """ Set maximum value. If `None`, there will be no maximum """
        if value is None:
            value = sys.float_info.max
        return super().setMaximum(value)
    
    def setRange(self, minimum:float=None, maximum:float=None):
        """ Set minimum and/or maximum """
        self.setMinimum(minimum)
        self.setMaximum(maximum)