from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, pyqtSignal, Qt
from PyQt5.QtGui import QColor
from typing import Any
import numpy as np

color = {
    'green': '#08EF0C',
    'red': '#EF0808',
    'yellow': '#dfef08'
}


class TableModel(QAbstractTableModel):
    '''
       Модель таблицы, тут описывается поведения самой таблицы и что с ней мождно делать 
    '''
    change_summary_row = pyqtSignal(QModelIndex)
    change_summary_column = pyqtSignal()
    
    def __init__(self) -> bool:
        super(TableModel, self).__init__()
        self._data = [[]]
        
        
    def update(self, data: np.ndarray) -> None:
        self.layoutAboutToBeChanged.emit()
        summary_rows = np.apply_over_axes(np.sum, data, axes=1)
        self._data = np.c_[data, summary_rows, np.add.accumulate(summary_rows)]
        self.layoutChanged.emit()

    def rowCount(self, parent: QModelIndex = ...) -> int:
        ''' Количество строк '''
        try:
            return self._data.shape[0]
        except AttributeError:
            return 0

    def columnCount(self, parent: QModelIndex = ...) -> int:
        ''' Количество колонок '''
        try:
            return self._data.shape[1]
        except AttributeError:
            return 0

    def data(self, index: QModelIndex, role: int = ...) -> Any:
        '''
            Отсюда береутся данные по Qt.ItemDataRole
        '''
        if index.isValid():
            
            value = self._data[index.row(), index.column()]
            
            if role == Qt.ItemDataRole.DisplayRole:
                return str(value)

            if role == Qt.ItemDataRole.BackgroundRole:
                return self.get_color(index)
                
        return None

    def setData(self, index: QModelIndex, value: Any, role: int = ...) -> bool:
        ''' 
            Тут и  происходит изменения данных
        '''
        if role == Qt.ItemDataRole.EditRole and value:
            self._data[index.row(), index.column()] = float(value)
            self.resum_row(index)
            return True
        

        return False

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        ''' По сути даем права на изменения всем колонкам, за исключения двух последних'''
        if index.isValid() and index.column() < self.columnCount() - 2:
            return Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
        else: 
            return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

    # def _first_resum_row(self) -> None:
    #     index = self.index(0, self.rowCount()-2)
    #     self.resum_row(self.index(0, ))
    def resum_row(self, index: QModelIndex = ...) -> None:
        '''
            Сумма строки
        '''
        # self.layoutAboutToBeChanged.emit()
        self._data[index.row(), -2] = sum(self._data[index.row()][:-2])
        self.resum_befor_column(index)
        self.change_summary_row.emit(index)


    def resum_befor_column(self, index: QModelIndex = ...) -> None:
        '''
            Пересчитываем сумму колонки
        '''
        self._data[:, -1] = np.add.accumulate(self._data[:, -2])
        self.change_summary_column.emit()
           
    def get_color(self, index: QModelIndex = ...) -> QColor:
        '''
            Проверяем меньше ли нуля цифра, и отдаем нужный цвет \n
            доп, последние две колонки окрашеваем в желтый
        '''
        value = self._data[index.row(), index.column()]
        
        if index.column() == 1:
            if int(value) > 0:
                return QColor(color.get('green'))

            if int(value) < 0:
                return QColor(color.get('red'))
                
        if index.column() > self.columnCount() - 3:
            return QColor(color.get('yellow'))
        
    def get_data(self) -> np.ndarray:
        '''Удаляем наши две колонки и возвращаем результат'''
        return np.delete(self._data, [-1, -2], axis=1)
        