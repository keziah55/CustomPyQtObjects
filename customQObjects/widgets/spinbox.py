"""
QSpinBox and QDoubleSpinBox subclasses that allow min and max to be essentially unset.
"""
from qtpy.QtWidgets import QSpinBox, QDoubleSpinBox
import sys

class SpinBox(QSpinBox):
    def setMinimum(self, value=None):
        """ Set minimum value. If `None`, there will be no minimum """
        if value is None:
            value = -2147483648
        return super().setMinimum(value)
    
    def setMaximum(self, value=None):
        """ Set maximum value. If `None`, there will be no maximum """
        if value is None:
            value = 2147483647
        return super().setMaximum(value)
    
    def setRange(self, minimum=None, maximum=None):
        """ Set minimum and/or maximum """
        self.setMinimum(minimum)
        self.setMaximum(maximum)
    
class DoubleSpinBox(QDoubleSpinBox):
    def setMinimum(self, value=None):
        """ Set minimum value. If `None`, there will be no minimum """
        if value is None:
            value = -sys.float_info.max
        return super().setMinimum(value)
    
    def setMaximum(self, value=None):
        """ Set maximum value. If `None`, there will be no maximum """
        if value is None:
            value = sys.float_info.max
        return super().setMaximum(value)
    
    def setRange(self, minimum=None, maximum=None):
        """ Set minimum and/or maximum """
        self.setMinimum(minimum)
        self.setMaximum(maximum)