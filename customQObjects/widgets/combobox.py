from qtpy.QtWidgets import QComboBox

class ComboBox(QComboBox):
    """ QComboBox with `items` property. """
    @property
    def items(self):
        """ Return list of text from all items. """
        return [self.itemText(idx) for idx in range(self.count())]