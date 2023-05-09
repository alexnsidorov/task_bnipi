from PyQt5.QtWidgets import QItemDelegate, QStyleOptionViewItem, QWidget
from PyQt5.QtCore import QModelIndex, Qt
from window.widgets import TBComboBox
from model import TableModel

class ComboDelegate(QItemDelegate):
    '''
        ComboDelegate - изменяет стиль измения ячейки
    '''
    
    def __init__(self, parent: None) -> None:
        super(ComboDelegate, self).__init__(parent)

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        ''' Определяет через какой виджет будем изменять ячейку '''
        return TBComboBox(parent)
    
    def setEditorData(self, editor: TBComboBox, index: QModelIndex) -> None:
        ''' Передаем из ячейки в виджет значения ячейки'''
        value = index.model().data(index, Qt.ItemDataRole.DisplayRole)
        if value:
            editor.setCurrentText(str(value))

    def setModelData(self, editor: TBComboBox, model: TableModel, index: QModelIndex) -> None:
        ''' Измененые данные вносим в ячейку '''
        model.setData(index, int(editor.currentText()), Qt.ItemDataRole.EditRole)