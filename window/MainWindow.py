from PyQt5.QtWidgets import QMainWindow, QAbstractItemView, QFileDialog
from PyQt5.QtCore import pyqtSlot, QItemSelection, Qt
from .Ui_MainWindow import Ui_MainWindow
from model import TableModel
from delegate import ComboDelegate
import work_with_file as wwf 


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None) -> None:
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self._selectionColumn = {}

        self.tableModel = TableModel()
        self.table.setModel(self.tableModel)
        
        #первая колонка будет изменяться по средствам Сombobox
        self.table.setItemDelegateForColumn(0, ComboDelegate(self))
        
        #подключаемя к слоту и выбираем сбособ выбора колонок
        self.table.selectionModel().selectionChanged.connect(self._repaint_graph)
        self.table.setSelectionMode(
            QAbstractItemView.SelectionMode.MultiSelection)
        
        self.open.clicked.connect(self._open_file)
        self.save.clicked.connect(self._save_file)

    pyqtSlot(QItemSelection, QItemSelection)
    def _repaint_graph(self, selected: QItemSelection, deselected: QItemSelection) -> None:
        '''
            перерисовываем график
        '''
        try:
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
        except KeyError:
            ...
            
        if len(self._selectionColumn) < 2:
            return
        
        self.graph.clear() #Чистим график
        
        #рисуем график
        for i in self._selectionColumn:
            self.graph.plot(self._selectionColumn.get(i))
            
    def _open_file(self) -> None:
        fileName, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "", "All Files (*);;")
        if fileName:
            self.tableModel.update(wwf.open_h5py(fileName))
            
            
    def _save_file(self) -> None:
        
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "All Files (*);;", options=options)
        if fileName:
            wwf.save_h5py(fileName, self.tableModel.get_data())
