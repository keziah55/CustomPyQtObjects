from PyQt5.QtCore import QSettings

class Settings(QSettings):
    
    def value(self, key, defaultValue=None, cast=None):
        v = super().value(key, defaultValue=defaultValue)
        if v == 'true':
            v = True
        elif v == 'false':
            v = False
        elif cast is not None:
            v = cast(v)
        return v