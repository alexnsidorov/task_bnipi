from PyQt5.QtWidgets import QMainWindow, QAbstractItemView
from PyQt5.QtCore import pyqtSlot, QItemSelection, Qt
from .Ui_MainWindow import Ui_MainWindow
from model import TableModel
from delegate import ComboDelegate
from pyqtgraph import PlotDataItem
import numpy as np
import work_with_file as wwf
import os


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None) -> None:
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self._selectionColumn = {}

        path_file = os.environ.get('path_file')
        value_from_file = wwf.values_from_file(path_file)
        
        if len(value_from_file) != 0:
            self._data = value_from_file
        else:
            self._data = np.array([
                [3, -5, 6, 1],
                [2, 4, -5, 10],
                [1, -3, 6, -15],
                [4, -1, 20, -15]
            ])

        tableModel = TableModel(self.add_columns_finaly(self._data))
        self.table.setModel(tableModel)
        self.table.setItemDelegateForColumn(0, ComboDelegate(self))
        self.table.selectionModel().selectionChanged.connect(self._show_graph)
        self.table.setSelectionMode(
            QAbstractItemView.SelectionMode.MultiSelection)

    def add_columns_finaly(self, data:np.ndarray) -> np.ndarray:
        ''' Создаем две колонки в массиве '''
        data = np.c_[data, np.zeros(data.shape[0], dtype=np.int8)]
        data = np.c_[data, np.zeros(data.shape[0], dtype=np.int8)]
        return data

    pyqtSlot(QItemSelection, QItemSelection)
    def _show_graph(self, selected: QItemSelection, deselected: QItemSelection) -> None:

        try:
            value = [int(x.data(Qt.ItemDataRole.DisplayRole))
                     for x in selected.indexes()]
            
            self._selectionColumn.update({
                selected.indexes()[0].column(): value
            })
        except IndexError:
            del self._selectionColumn[deselected.indexes()[0].column()]

        if len(self._selectionColumn) < 2:
            return
        self.graph.clear()
        for i in self._selectionColumn:
            self.graph.plot(self._selectionColumn.get(i))
