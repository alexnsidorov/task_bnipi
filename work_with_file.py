import numpy as np
from PyQt5.QtCore import QModelIndex, pyqtSignal
import h5py
import os


def values_from_file(path: str = None) -> np.ndarray:
    try:
        with open(path) as f:
            return np.loadtxt(f)
            # return values if len(values) != 0 else None
    except FileNotFoundError:
        return None
    except ValueError:
        return None


class with_h5py_matrix:
    
    change_summary_row = pyqtSignal(QModelIndex)
    change_summary_column = pyqtSignal()
    base_group: str = 'Base_Group'
    default_sub_group: str = 'default'
    column_sum_row: str = 'column_sum_row'
    column_sum_column: str = 'column_sum_column'

    def __init__(self, file_name):
        '''Инцилизация класса, тут так же не большие проверки'''
        if os.path.exists(file_name):
            self._file_name = file_name

            self.check_data()
    
            self._default_shape = self._get_default_shape()
            self.create_column_sum_row()
            self.create_column_sum_column()
        else:
            raise FileExistsError(F"Не нашли файл: {file_name}")

    def check_data(self):
        '''
            проверка по индексам
        '''
        with h5py.File(self._file_name, 'a') as f:
            try:
                data = f[self.base_group]
                data = data[self.default_sub_group]
            except KeyError:
                raise KeyError(
                    F'Нет групп: {self.base_group}, {self.default_sub_group}')

    def __del__(self):
        '''При удалении класса удаляются и то что мы насчитали'''
        try:
            with h5py.File(self._file_name, 'a') as f:
                del f[self.base_group][self.column_sum_row]
                del f[self.base_group][self.column_sum_column]
        except KeyError:
            ...

    def data(self, index: QModelIndex = ...) -> float:
        '''Через эту функцию вытаскиваются данные'''
        _range = index.column() - self._default_shape[1]

        sub_group = None

        if index:
            if _range not in (0, 1):
                sub_group = self.default_sub_group
            elif _range == 0:
                sub_group = self.column_sum_row
            elif _range == 1:
                sub_group = self.column_sum_column

            if sub_group:
                return self._get_data(sub_group, index)

        return 0.0

    
    def _get_data(self, sub_group: str = None, index: QModelIndex = None) -> float:
        with h5py.File(self._file_name, 'r') as f:
            if sub_group and not index:
                return np.array(f[self.base_group][sub_group])

            if sub_group in self.default_sub_group:
                try:
                    return f[self.base_group][sub_group][index.row()][index.column()]
                except IndexError:
                    return 0.0

            if sub_group in (self.column_sum_column, self.column_sum_row):
                try:
                    return f[self.base_group][sub_group][index.row(), 0]
                except IndexError:
                    return 0.0

            return 0.0
        
    def create_column_sum_row(self) -> None:
        '''Создаем колонку для подчета строк'''
        with h5py.File(self._file_name, 'a') as f:
            try:
                summary_rows = np.apply_over_axes(np.sum, np.array(
                    self._get_data(self.default_sub_group)), axes=1)
                f[self.base_group].create_dataset(
                    self.column_sum_row, data=summary_rows)
            except ValueError:
                ...

    def create_column_sum_column(self) -> None:
        '''Создаем колонку для подчета колонки'''
        with h5py.File(self._file_name, 'a') as f:
            try:
                summary_rows = np.add.accumulate(
                    self._get_data(self.column_sum_row))
                f[self.base_group].create_dataset(
                    self.column_sum_column, data=summary_rows)
            except ValueError:
                ...

    def change_value(self, value: float, index: QModelIndex) -> None:
        '''Изменение основного блока данных'''
        with h5py.File(self._file_name, 'a') as f:
            try:
                f[self.base_group][self.default_sub_group][index.row(),
                                                           index.column()] = float(value)
                self.resum_row(index)
            except ValueError:
                ...


    def _get_default_shape(self) -> tuple:
        '''Берем размер матрицы из блока с default_sub_group'''
        with h5py.File(self._file_name, 'r') as f:
            return tuple(f[self.base_group][self.default_sub_group].shape)

    def shape(self) -> tuple:
        return (self._default_shape[0], self._default_shape[1] + 2)

    def resum_row(self, index: QModelIndex = ...) -> None:
        '''
            Сумма строки
        '''

        with h5py.File(self._file_name, 'a') as f:
            f[self.base_group][self.column_sum_row][index.row(), 0] = sum(
                f[self.base_group][self.default_sub_group][index.row()])
            self.resum_column(index)

    def resum_column(self, index: QModelIndex = ...) -> None:
        '''
            Пересчитываем сумму колонки
        '''
        with h5py.File(self._file_name, 'a') as f:
            print(f[self.base_group][self.column_sum_column])
            f[self.base_group][self.column_sum_column][:, 0] = np.add.accumulate(
                f[self.base_group][self.column_sum_row])[:, 0]
