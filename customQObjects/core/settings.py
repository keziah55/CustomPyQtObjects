from qtpy.QtCore import QSettings

class Settings(QSettings):
    """ 
    [QSettings](https://doc.qt.io/qt-6/qsettings.html) subclass that provides 
    [value][customQObjects.core.Settings.value] method that will cast
    "true" and "false" to True or False, or will cast the returned value to
    the given type.
    """
    def value(self, key, defaultValue=None, cast=None):
        """ 
        Get value from settings. If value is "true" or "false", return True or False.
            
        Parameters
        ----------
        key : str
            Setting to be returned
        defaultValue : object, optional
            If `key` is not in the settings, return `defaultValue`. Default
            is None
        cast : type, optional
            If provided, cast the value to the given type
        """
        v = super().value(key, defaultValue=defaultValue)
        if v == 'true':
            v = True
        elif v == 'false':
            v = False
        elif cast is not None:
            v = cast(v)
        return v