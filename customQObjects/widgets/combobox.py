from qtpy.QtWidgets import QComboBox
from qtpy.QtCore import QAbstractListModel, Qt
from typing import NamedTuple


class ComboBoxModel(QAbstractListModel):
    """
    [QAbstractListModel](https://doc.qt.io/qt-6/qabstractlistmodel.html)
    that takes a list of
    [NamedTuples](https://docs.python.org/3/library/typing.html#typing.NamedTuple)
    with field names 'name' and 'value'.

    [data][customQObjects.widgets.ComboBoxModel.data] will return the `name` when
    asked for the [Qt.DisplayRole](https://doc.qt.io/qt-6/qt.html#ItemDataRole-enum)
    and the `value` when asked for the
    [Qt.UserRole](https://doc.qt.io/qt-6/qt.html#ItemDataRole-enum).
    """

    def __init__(self, values: list[NamedTuple], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.values = values

    def headerData(self):
        return None

    def rowCount(self, column=None):
        return len(self.values)

    def data(self, idx, role):
        """
        Return the data at index `idx`.

        If `role` is [Qt.DisplayRole](https://doc.qt.io/qt-6/qt.html#ItemDataRole-enum), return the
        NamedTuple's `name`.
        If `role` is [Qt.UserRole](https://doc.qt.io/qt-6/qt.html#ItemDataRole-enum), return the
        NamedTuple's `value`.
        """
        if not idx.isValid():
            return None

        value = self.values[idx.row()]

        if role == Qt.DisplayRole:
            return value.name

        elif role == Qt.UserRole:
            return value.value


class ComboBox(QComboBox):
    """
    [QComboBox](https://doc.qt.io/qt-6/qcombobox.html) with
    [items][customQObjects.widgets.ComboBox.items] property and ability to
    automatically create item model.

    Parameters
    ----------
    values : list[NamedTuple], optional
        If provided, this will be used to display and return data. The tuple
        fields should be 'name' and 'value'; 'name' is displayed as text and
        'value' is returned by [value][customQObjects.widgets.combobox.ComboBox.value].
        If not provided, [value][customQObjects.widgets.combobox.ComboBox.value] will return the
        current text.
    model : QAbstractListModel, optional
        Model to use. If not provided, a [ComboBoxModel][customQObjects.widgets.ComboBoxModel]
        is created that returns the 'name' and 'value' from the `values` list when asked for the
        [Qt.DisplayRole](https://doc.qt.io/qt-6/qt.html#ItemDataRole-enum) and
        [Qt.UserRole](https://doc.qt.io/qt-6/qt.html#ItemDataRole-enum) respectively
    args :
        [QComboBox](https://doc.qt.io/qt-6/qcombobox.html) args
    kwargs :
        [QComboBox](https://doc.qt.io/qt-6/qcombobox.html) kwargs
    """

    def __init__(self, *args, values: list[NamedTuple] = None, model=None, **kwargs):
        super().__init__(*args, **kwargs)
        if model is None:
            model = ComboBoxModel
        if values is not None:
            mdl = model(values)
            self.setModel(mdl)
        self._values = values

    @property
    def items(self):
        """Return list of text from all items."""
        return [self.itemText(idx) for idx in range(self.count())]

    @property
    def value(self):
        """Return current value"""
        if self._values is None:
            return self.currentText()
        else:
            return self.itemData(self.currentIndex(), Qt.UserRole)
