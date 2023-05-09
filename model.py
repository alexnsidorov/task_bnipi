from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, pyqtSignal, Qt
from PyQt5.QtGui import QBrush
from typing import Any, Dict
import numpy as np


class TableModel(QAbstractTableModel):
    returnData = pyqtSignal(QModelIndex, int) 
    def __init__(self, parent: None) -> bool:
        super(TableModel, self).__init__(parent)
        self._data: np.ndarray = None
        self._colors: np.ndarray = None


    def update(self, dataIn: np.ndarray) -> None:
        self._data = dataIn
        self._colors = np.full(dataIn.shape, Qt.GlobalColor.green) 


    def rowCount(self, parent: QModelIndex = ...) -> int:
        try:
            return self._data.shape[0]
        except AttributeError:
            return 0

    def columnCount(self, parent: QModelIndex = ...) -> int:
        try:
            return self._data.shape[1]
        except AttributeError:
            return 0

    def data(self, index: QModelIndex, role: int = ...) -> Any:
        if index.isValid():
            if role == Qt.ItemDataRole.DisplayRole:
                value = self._data[index.row(), index.column()]
                return str(value)
                
            if role == Qt.ItemDataRole.EditRole:
                color = self._colors[index.row(), index.column()]
                print(color)
                if color is not None:
                    return color
        return None
    
    def setData(self, index: QModelIndex, value: Any, role: int = ...) -> bool:
        if role == Qt.ItemDataRole.EditRole and value:
            print(value)
            self._data[index.row(), index.column()] = int(value)
            return True

        return False

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:

        if index.isValid():
            # self.change_color(index)
            return Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled
        else:
            return Qt.ItemFlag.ItemIsEnabled
        
    def change_color(self, index: QModelIndex, color: int):
        ix = self.index(index.row(), index.column())
        print(index.row(), index.column())
        self._colors[index.row(), index.column()] = int(color)
        self.dataChanged.emit(ix, ix, (Qt.ItemDataRole.BackgroundColorRole,))