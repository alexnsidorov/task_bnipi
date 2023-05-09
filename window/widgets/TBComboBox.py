from PyQt5.QtWidgets import QComboBox, QWidget
from PyQt5.QtCore import pyqtSignal, pyqtSlot

class TBComboBox(QComboBox):
    selectedValue = pyqtSignal(int)
    def __init__(self, parent: QWidget = None, max_count: int = 5) -> None:
        super(TBComboBox, self).__init__(parent)

        self.addItems([str(x) for x in range(1, max_count + 1)])
        self.currentTextChanged.connect(self._currentTextChanged)

    @pyqtSlot(str)
    def _currentTextChanged(self, value):
        self.selectedValue.emit(int(value))