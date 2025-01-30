from qtpy.QtWidgets import QDialog
from qtpy.QtCore import QTimer


class TimerDialog(QDialog):
    """
    [QDialog](https://doc.qt.io/qt-5/qdialog.html) that will timeout after a given number of
    milliseconds.

    Parameters
    ----------
    timeout : int
        Number of milliseconds for the dialog to be shown. Default is 3000.
    """

    def __init__(self, timeout=3000):
        super().__init__()
        self._timeout = timeout
        self.timer = QTimer()
        self.timer.setInterval(timeout)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.accept)

    @property
    def timeout(self):
        """Return current timeout (ms)"""
        return self._timeout

    def exec_(self, *args, **kwargs):
        """Show the dialog and start the timer."""
        self.timer.start()
        super().exec_(*args, **kwargs)

    def setTimeout(self, timeout):
        """Update `timeout`"""
        self._timeout = timeout
        self.timer.setInterval(timeout)
