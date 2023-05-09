from PyQt5.QtWidgets import QItemDelegate, QStyledItemDelegate, QStyleOptionViewItem, QWidget
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import QModelIndex, Qt
from window.widgets import TBComboBox
from model import TableModel

class ComboDelegate(QItemDelegate):
    def __init__(self, parent: None) -> None:
        super(ComboDelegate, self).__init__(parent)

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        return TBComboBox(parent)
    
    def setEditorData(self, editor: TBComboBox, index: QModelIndex) -> None:
        value = index.model().data(index, Qt.ItemDataRole.DisplayRole)
        if value:
            editor.setCurrentText(str(value))

    def setModelData(self, editor: TBComboBox, model: TableModel, index: QModelIndex) -> None:
        model.setData(index, int(editor.currentText()), Qt.ItemDataRole.EditRole)


class RedCellDelegate(QStyledItemDelegate):
    def __init__(self, parent= None) -> None:
        super(RedCellDelegate, self).__init__()

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        painter.setBackground(QColor('red'))