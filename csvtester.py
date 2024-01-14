from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import QCoreApplication


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CSV Comparator")


app = QCoreApplication.instance()
if app is None:
    app = QApplication([])

window = MainWindow()
window.show()
app.exec()