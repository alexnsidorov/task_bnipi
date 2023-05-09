from PyQt5.QtWidgets import QMainWindow, QAbstractItemView
from PyQt5.QtCore import pyqtSlot, QItemSelection, Qt
from .Ui_MainWindow import Ui_MainWindow
from model import TableModel
from delegate import ComboDelegate
import numpy as np
import work_with_file as wwf
import os


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None) -> None:
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self._selectionColumn = {}

        #берем данные из файлика
        path_file = os.environ.get('path_file')
        value = wwf.values_from_file(path_file)
        
        #проверяем есть ли данные
        if 'ndarray' not in str(type(value)):
            value = np.array([
                [3, -5, 6, 1],
                [2, 4, -5, 10],
                [1, -3, 6, -15],
                [4, -1, 20, -15]
            ])

        tableModel = TableModel(self.add_columns_finaly(value))
        self.table.setModel(tableModel)
        
        #первая колонка будет изменяться по средствам Сombobox
        self.table.setItemDelegateForColumn(0, ComboDelegate(self))
        
        #подключаемя к слоту и выбираем сбособ выбора колонок
        self.table.selectionModel().selectionChanged.connect(self._repaint_graph)
        self.table.setSelectionMode(
            QAbstractItemView.SelectionMode.MultiSelection)

    def add_columns_finaly(self, data:np.ndarray) -> np.ndarray:
        ''' Создаем две колонки в массиве '''
        data = np.c_[data, np.zeros(data.shape[0], dtype=np.int8)]
        data = np.c_[data, np.zeros(data.shape[0], dtype=np.int8)]
        return data

    pyqtSlot(QItemSelection, QItemSelection)
    def _repaint_graph(self, selected: QItemSelection, deselected: QItemSelection) -> None:
        '''
            перерисовываем график
        '''
        try:
            #заносим массив вырбранной колонки
            value = [int(x.data(Qt.ItemDataRole.DisplayRole))
                     for x in selected.indexes()]
            
            self._selectionColumn.update({
                selected.indexes()[0].column(): value
            })
        except IndexError:
            #deselected 
            del self._selectionColumn[deselected.indexes()[0].column()]

        if len(self._selectionColumn) < 2:
            return
        
        self.graph.clear() #Чистим график
        
        #рисуем график
        for i in self._selectionColumn:
            self.graph.plot(self._selectionColumn.get(i))
