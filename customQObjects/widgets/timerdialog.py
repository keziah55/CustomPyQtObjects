from qtpy.QtWidgets import QDialog
from qtpy.QtCore import QTimer

class TimerDialog(QDialog):
    """ [QDialog](https://doc.qt.io/qt-5/qdialog.html) that will timeout after a given number of milliseconds. 
    
        Parameters
        ----------
        timeout : int
            Number of milliseconds for the dialog to be shown. Default is 3000.
    """
    
    def __init__(self, timeout=3000):
        super().__init__()
        self.timer = QTimer()
        self.timer.setInterval(timeout)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.accept)
        
    def exec_(self, *args, **kwargs):
        """ Show the dialog and start the timer. """
        self.timer.start()
        super().exec_(*args, **kwargs)
        