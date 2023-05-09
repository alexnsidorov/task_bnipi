from PyQt5.QtWidgets import QTableView, QStyle
from PyQt5.QtCore import pyqtSlot, QModelIndex, Qt
from PyQt5.QtGui import QStandardItemModel 
from delegate import ComboDelegate, RedCellDelegate
from model import TableModel
import numpy as np


class TBTableView(QTableView):

    def __init__(self, parent):
        super(TBTableView, self).__init__(parent)
        self.tableModel = TableModel(self)
        # self.tableModel.returnData.connect(self._changeColor)

        self.setModel(self.tableModel)
        self.setItemDelegateForColumn(0, ComboDelegate(self))
        # self.setItemDelegate(RedCellDelegate(self))
        # self.setStyle()
        
    def setData(self, dataIn: np.ndarray) -> None:
        self.tableModel.update(dataIn)
        self.tableModel.change_color(self.tableModel.index(1, 1), Qt.GlobalColor.red)


    # def set_cell_color(self, index: QModelIndex,  value: int):
    #     if value < 0:
    #         
    #     elif value > 0:
    #         self.tableModel.change_color(index, Qt.GlobalColor.green)