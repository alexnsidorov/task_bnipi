from PyQt5.QtWidgets import QMainWindow, QAbstractItemView, QMessageBox
from PyQt5.QtCore import pyqtSlot, QItemSelection, Qt
from .Ui_MainWindow import Ui_MainWindow
from .widgets import show_warning
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
                [1, -3, 1, -15],
                [4, -1, 20, -15]
            ])
        else:
            show_warning('Не понятный массив', 'Где-то ошибка в двумерном массиве \n Исправте файл')

        tableModel = TableModel()
        tableModel.update(value)
        self.table.setModel(tableModel)
        
        #первая колонка будет изменяться по средствам Сombobox
        self.table.setItemDelegateForColumn(0, ComboDelegate(self))
        
        #подключаемя к слоту и выбираем сбособ выбора колонок
        self.table.selectionModel().selectionChanged.connect(self._repaint_graph)
        self.table.setSelectionMode(
            QAbstractItemView.SelectionMode.MultiSelection)

    pyqtSlot(QItemSelection, QItemSelection)
    def _repaint_graph(self, selected: QItemSelection, deselected: QItemSelection) -> None:
        '''
            перерисовываем график
        '''
        try:
            if len(selected.indexes()) != selected.indexes()[0].model().rowCount():
                return
            
            lfunc = np.vectorize(lambda x: float(x.data(Qt.ItemDataRole.DisplayRole)))
            
            #заносим массив вырбранной колонки
            self._selectionColumn.update({
                selected.indexes()[0].column(): lfunc(np.array(selected.indexes()))
            })
        except IndexError:
            #deselected 
            try:
                if len(deselected.indexes()) != deselected.indexes()[0].model().rowCount():
                    return
                
                del self._selectionColumn[deselected.indexes()[0].column()]
            except IndexError:
                ...
                
        if len(self._selectionColumn) != 2:
            return
        
        self.graph.clear() #Чистим график
        
        #рисуем график
        values = list(self._selectionColumn.values())
        self.graph.plot(values[0], values[1], pen='#42f542')
