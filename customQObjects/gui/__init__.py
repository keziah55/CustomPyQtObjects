from qtpy.QtGui import QIcon, QBrush, QColor

def getIconFromTheme(name: str) -> QIcon:
    """ 
    If [QIcon.hasThemeIcon(name)](https://doc.qt.io/qt-6/qicon.html#hasThemeIcon) is True, 
    return [QIcon.fromTheme(name)](https://doc.qt.io/qt-6/qicon.html#fromTheme). 
    
    Otherwise, return None.
    """
    if QIcon.hasThemeIcon(name):
        return QIcon.fromTheme(name)
    else:
        return None
    
def makeBrush(arg) -> QBrush:
    """ 
    Return a [QBrush](https://doc.qt.io/qt-6/qbrush.html) from `arg`.
    
    `arg` can be a [QBrush](https://doc.qt.io/qt-6/qbrush.html), [QColor](https://doc.qt.io/qt-6/qcolor.html) 
    or any valid [QColor](https://doc.qt.io/qt-6/qcolor.html) constructor arg.
    """
    if isinstance(arg, QBrush):
        return arg
    if isinstance(arg, QColor):
        return QBrush(arg)
    if isinstance(arg, str):
        try:
            color = QColor(arg)
        except:
            raise ValueError(f"Could not construct QBrush from '{arg}'")
        else:
            return QBrush(color)
    return None
    
__all__ = ["getIconFromTheme", "makeBrush"]