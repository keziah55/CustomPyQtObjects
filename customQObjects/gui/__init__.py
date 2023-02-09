from qtpy.QtGui import QIcon, QBrush, QColor

def getIconFromTheme(name):
    """ 
    If `QIcon.hasThemeIcon(name)` is True, return the `QIcon.fromTheme(name)`. 
    
    Otherwise, return None.
    """
    if QIcon.hasThemeIcon(name):
        return QIcon.fromTheme(name)
    else:
        return None
    
def makeBrush(value):
    """ 
    Return a [QBrush](https://doc.qt.io/qt-6/qbrush.html) from `value`.
    
    `value` can be a [QBrush](https://doc.qt.io/qt-6/qbrush.html), [QColor](https://doc.qt.io/qt-6/qcolor.html) 
    or any valid [QColor](https://doc.qt.io/qt-6/qcolor.html) constructor arg.
    """
    if isinstance(value, QBrush):
        return value
    if isinstance(value, QColor):
        return QBrush(value)
    if isinstance(value, str):
        try:
            color = QColor(value)
        except:
            raise ValueError(f"Could not construct QBrush from '{value}'")
        else:
            return QBrush(color)
    return None
    
__all__ = ["getIconFromTheme"]