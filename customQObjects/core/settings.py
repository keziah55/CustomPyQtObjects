from PyQt5.QtCore import QSettings

class Settings(QSettings):
    """ QSettings subclass that provides :meth:`value` method that will cast
        "true" and "false" to True or False, or will cast the returned value to t
        he given type.
    """
    def value(self, key, defaultValue=None, cast=None):
        """ Get value from settings. If value is "true" or "false", return True
            or False.
            
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