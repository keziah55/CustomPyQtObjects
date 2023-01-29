from qtpy.QtWidgets import QComboBox
from qtpy.QtCore import QAbstractListModel, Qt
from typing import NamedTuple

class ComboBoxModel(QAbstractListModel):
    """ QAbstractListModel that takes a list of NamedTuples with field names 'name' and 'value'
    
        :meth:`data` will reurn the `name` when asked for the Qt.DisplayRole
        or the 'value' when asked for the Qt.UserRole.
    """
    def __init__(self, values:list[NamedTuple], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.values = values 
        
    def headerData(self):
        return None
    
    def rowCount(self, column=None):
        return len(self.values)
    
    def data(self, idx, role):
        """ Return the data at index `idx`. 
        
            If `role` is `Qt.DisplayRole`, return the NamedTuple's `name`.
            If `role` is `Qt.UserRole`, return the NamedTuple's `value`.
        """
        if not idx.isValid():
            return None
        
        value = self.values[idx.row()]
        
        if role == Qt.DisplayRole:
            return value.name
        
        elif role == Qt.UserRole:
            return value.value

class ComboBox(QComboBox):
    """ QComboBox with `items` property and ability to automatically create item model.
    
        If list of NamedTuples passed as `values`, this will be used to display
        and return data. The tuple fields should be 'name' and 'value'; 'name' 
        will be displayed as text and 'value' will be returned by :meth:`value`.
        
        If `values` not provided, :meth:`value` will return the current text.
    """
    def __init__(self, *args, values:list[NamedTuple]=None, model=None, **kwargs):
        super().__init__(*args, **kwargs)
        if model is None:
            model = ComboBoxModel
        if values is not None:
            mdl = model(values)
            self.setModel(mdl)
        self._values = values
    
    @property
    def items(self):
        """ Return list of text from all items. """
        return [self.itemText(idx) for idx in range(self.count())]
    
    @property
    def value(self):
        """ Return current value """
        if self._values is None:
            return self.currentText()
        else:
            return self.itemData(self.currentIndex(), Qt.UserRole)