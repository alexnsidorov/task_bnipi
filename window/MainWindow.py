from PyQt5.QtWidgets import QMainWindow, QAbstractItemView, QFileDialog
from PyQt5.QtCore import pyqtSlot, QItemSelection, Qt
from .Ui_MainWindow import Ui_MainWindow
from model import TableModel
from delegate import ComboDelegate
import work_with_file as wwf
import numpy as np


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None) -> None:
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self._selectionColumn = {}

        self.tableModel = TableModel()
        self.table.setModel(self.tableModel)

        # первая колонка будет изменяться по средствам Сombobox
        self.table.setItemDelegateForColumn(0, ComboDelegate(self))

        # подключаемя к слоту и выбираем сбособ выбора колонок
        self.table.selectionModel().selectionChanged.connect(self._repaint_graph)
        self.table.setSelectionMode(
            QAbstractItemView.SelectionMode.MultiSelection)

        self.open.clicked.connect(self._open_file)
        # self.save.clicked.connect(self._save_file)

    pyqtSlot(QItemSelection, QItemSelection)

    def _repaint_graph(self, selected: QItemSelection, deselected: QItemSelection) -> None:
        '''
            перерисовываем график
        '''

        self._prepare_data(selected, deselected)

        if len(self._selectionColumn) != 2:
            return

        self.graph.clear()  # Чистим график

        # рисуем график
        values = list(self._selectionColumn.values())
        self.graph.plot(values[0], values[1], pen='#42f542')

    def _prepare_data(self, selected: QItemSelection, deselected: QItemSelection):
        '''
            тут заносим и удаляем данные в dict _selectionColumn 
        '''
        try:
            if len(selected.indexes()) != selected.indexes()[0].model().rowCount():
                return

            lfunc = np.vectorize(lambda x: float(
                x.data(Qt.ItemDataRole.DisplayRole)))

            # заносим массив вырбранной колонки
            self._selectionColumn.update({
                selected.indexes()[0].column(): lfunc(np.array(selected.indexes()))
            })
        except IndexError:
            # deselected
            try:
                if len(deselected.indexes()) != deselected.indexes()[0].model().rowCount():
                    return

                del self._selectionColumn[deselected.indexes()[0].column()]
            except IndexError:
                ...
            except KeyError:
                ...

    def _open_file(self) -> None:
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Открыть файл", "", "All Files (*);;")

        if fileName:
            self.tableModel.update(fileName)

    def _save_file(self) -> None:

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(
            self, "Сохранить файл", "", "All Files (*);;", options=options)
        if fileName:
            wwf.save_h5py(fileName, self.tableModel.get_data())
