from qtpy.QtGui import QIcon

def getIconFromTheme(name):
    """ If `QIcon.hasThemeIcon(name)` is True, return the `QIcon.fromTheme(name)`. 
    
        Otherwise, return None.
    """
    if QIcon.hasThemeIcon(name):
        return QIcon.fromTheme(name)
    else:
        return None
    
__all__ = ["getIconFromTheme"]