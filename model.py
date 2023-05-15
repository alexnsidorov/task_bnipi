from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, pyqtSignal, Qt
from PyQt5.QtGui import QColor
from typing import Any
import numpy as np
import h5py
from work_with_file import with_h5py_matrix

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
    
    _h5py_matrix: with_h5py_matrix = None

    def __init__(self) -> bool:
        super(TableModel, self).__init__()
        self._data = [[]]
        self._file_name = None
        
        
    def update(self, file_name) -> None:
        self.layoutAboutToBeChanged.emit()
        self._h5py_matrix = with_h5py_matrix(file_name)             
        
        self.layoutChanged.emit()
        
        
    def rowCount(self, parent: QModelIndex = ...) -> int:
        ''' Количество строк '''
        try:
            return self._h5py_matrix.shape()[0]
        except AttributeError:
            return 0

    def columnCount(self, parent: QModelIndex = ...) -> int:
        ''' Количество колонок '''
        try:
            return self._h5py_matrix.shape()[1]
        except AttributeError:
            return 0
        
    def data(self, index: QModelIndex, role: int = ...) -> Any:
        '''
            Отсюда береутся данные по Qt.ItemDataRole
        '''
        if index.isValid():
            
            value = self._h5py_matrix.data(index)
            if role == Qt.ItemDataRole.DisplayRole:
                return str(value)
                    

            if role == Qt.ItemDataRole.BackgroundRole:
                return self.get_color(value, index)
                
        return None

    def setData(self, index: QModelIndex, value: Any, role: int = ...) -> bool:
        ''' 
            Тут и  происходит изменения данных
        '''
        if role == Qt.ItemDataRole.EditRole and value:
            try:
                self._h5py_matrix.change_value(value, index)
                return True
            except ValueError:
                return False

        return False

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        ''' По сути даем права на изменения всем колонкам, за исключения двух последних'''
        if index.isValid() and index.column() < self.columnCount() - 2:
            return Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
        else: 
            return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
           
    def get_color(self, value, index: QModelIndex = ..., ) -> QColor:
        '''
            Проверяем меньше ли нуля цифра, и отдаем нужный цвет \n
            доп, последние две колонки окрашеваем в желтый
        '''
        
        if index.column() == 1:
            if int(value) > 0:
                return QColor(color.get('green'))

            if int(value) <= 0:
                return QColor(color.get('red'))
                
        if index.column() > self.columnCount() - 3:
            return QColor(color.get('yellow'))
        
    def get_data(self) -> np.ndarray:
        '''Удаляем наши две колонки и возвращаем результат'''
        return np.delete(self._data, [-1, -2], axis=1)
        