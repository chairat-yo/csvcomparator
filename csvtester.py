import sys
import csv
from PyQt6.QtCore import QCoreApplication
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget,
    QTableWidgetItem, QDockWidget, QFormLayout,
    QLineEdit, QWidget, QPushButton, QSpinBox,
    QMessageBox, QToolBar, QMessageBox, QFileDialog, QCheckBox, QLabel
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QAction
from pathlib import Path


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('CSV Comparator')
        self.setWindowIcon(QIcon('./assets/usergroup.png'))
        self.setGeometry(100, 100, 600, 400)

        self.table1 = QTableWidget(self)
        self.setCentralWidget(self.table1)

        # self.table2 = QTableWidget(self)

        dock = QDockWidget('Files to Compare')
        dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

        # create form
        form = QWidget()
        layout = QFormLayout(form)
        form.setLayout(layout)

        # row1
        self.file_1 = QLineEdit('File1', form)
        btn_file_1 = QPushButton('Browse')
        btn_file_1.clicked.connect(self.open_file1_dialog)
        layout.addRow(self.file_1, btn_file_1)

        # row2
        self.file_2 = QLineEdit('File2', form)
        btn_file_2 = QPushButton('Browse')
        btn_file_2.clicked.connect(self.open_file2_dialog)
        layout.addRow(self.file_2, btn_file_2)

        # row3
        btn_compare = QPushButton('Compare')
        btn_compare.clicked.connect(self.compare_file)
        layout.addRow(btn_compare)

        # delimeterLabel = QLabel("Delimeter", self)
        self.delimeter = QLineEdit('Delimeter')
        self. delimeter.setText('|')
        layout.addRow('Delimeter:', self.delimeter)

        headerCheck = QCheckBox("Has Header", self)
        headerCheck.setChecked(True)
        layout.addRow(headerCheck)

        # add toolbar
        toolbar = QToolBar('main toolbar')
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        dock.setWidget(form)

    def compare_file(self):
        filename = self.file_1.text();
        csvFile = open(filename)
        csvReader = csv.reader(csvFile, delimiter=self.delimeter.text())
        csvData = list(csvReader)

        self.table1.setColumnCount(len(csvData[0]))

        self.table1.setHorizontalHeaderLabels(csvData[0])
        self.table1.setRowCount(len(csvData) - 1)

        row = 0
        for r in csvData:
            col = 0
            for c in r:
                # print('column: ', col, 'columnData: ', c)
                if (row != 0):
                    self.table1.setItem(row - 1, col, QTableWidgetItem(c))
                    col += 1
            row += 1
        # print(csvData)
        print('column counts: ', len(csvData[0]))
        print('csvData length: ', len(csvData))

    def open_file1_dialog(self):
        filename, ok = QFileDialog.getOpenFileName(
            self,
            "Select a File",
            directory="C:\\Users\\Admin\\Desktop\\csv"
        )
        print('filename: ', filename, ' ok:', ok)
        if filename:
            path = Path(filename)
            self.file_1.setText(str(path))

    def open_file2_dialog(self):
        filename, ok = QFileDialog.getOpenFileName(
            self,
            "Select a File",
            "D:\\icons\\avatar\\"
        )
        print('filename: ', filename, ' ok:', ok)
        if filename:
            path = Path(filename)
            self.file_2.setText(str(path))
        # dialog = QFileDialog(self)
        # dialog.setDirectory(r'C:\images')
        # dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        # dialog.setNameFilter("Images (*.csv *.dat)")
        # dialog.setViewMode(QFileDialog.ViewMode.List)
        # if dialog.exec():
        #     filenames = dialog.selectedFiles()
        #     if filenames:
        #         self.file_list.addItems([str(Path(filename)) for filename in filenames])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
