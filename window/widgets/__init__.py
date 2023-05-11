from .TBComboBox import TBComboBox
from PyQt5.QtWidgets import QMessageBox
# from .TBTableView import TBTableView
 

__all__ = ['TBComboBox', 'TBTableView']


def show_warning(title: str, text: str) -> None:
   msgBox = QMessageBox()
   msgBox.setIcon(QMessageBox.Icon.Warning)
   msgBox.setText(text)
   msgBox.setWindowTitle(title)
   msgBox.setStandardButtons(QMessageBox.Ok)
   msgBox.exec()