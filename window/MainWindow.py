from PyQt5.QtWidgets import QMainWindow
from .Ui_MainWindow import Ui_MainWindow
from PyQt5 import uic
import numpy as np


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None) -> None:
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        data = np.array([
            [3, -5, 6],
            [2, 4, -5],
            [1, -3, 6]
        ])
        self.table.setData(data)

        
