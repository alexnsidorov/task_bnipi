from PyQt5.QtWidgets import QApplication
from window.MainWindow import MainWindow
import sys, os


def main():
    app = QApplication(sys.argv)

    os.environ.update({
        'path_file': 'array.txt'
    })
    
    main_window = MainWindow()
    main_window.show()
    
    
    app.exec()

if __name__ == '__main__':
    main()