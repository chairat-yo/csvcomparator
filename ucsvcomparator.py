import os.path
import sys
import csv
import pandas as p
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg
from pathlib import Path


class MainWindow(qtw.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('CSV Comparator')
        self.setWindowIcon(qtg.QIcon('./assets/usergroup.png'))
        self.setGeometry(100, 100, 1080, 600)

        table_layout = qtw.QHBoxLayout()
        self.central_widget = qtw.QWidget(self)
        self.central_widget.setLayout(table_layout)
        self.setCentralWidget(self.central_widget)

        # table1
        self.table1 = qtw.QTableWidget()
        self.table1.setSortingEnabled(True)
        table_layout.addWidget(self.table1)

        # table2
        self.table2 = qtw.QTableWidget()
        self.table2.setSortingEnabled(True)
        table_layout.addWidget(self.table2)

        # scroll
        self.table1.verticalScrollBar().valueChanged.connect(self.table2.verticalScrollBar().setValue)
        self.table2.verticalScrollBar().valueChanged.connect(self.table1.verticalScrollBar().setValue)

        self.table1.horizontalScrollBar().valueChanged.connect(self.table2.horizontalScrollBar().setValue)
        self.table2.horizontalScrollBar().valueChanged.connect(self.table1.horizontalScrollBar().setValue)

        # sorting
        self.table1.horizontalHeader().sectionClicked.connect(self.sort_data)
        # self.table1.horizontalHeader().sectionClicked.connect(self.table2.sortByColumn)
        # self.table2.horizontalHeader().sectionClicked.connect(self.table1.sortByColumn)

        dock = qtw.QDockWidget('Files to Compare')
        dock.setFeatures(qtw.QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.addDockWidget(qtc.Qt.DockWidgetArea.RightDockWidgetArea, dock)

        ##############################################
        #################create form##################
        ##############################################
        form = qtw.QWidget()
        layout = qtw.QFormLayout(form)
        form.setLayout(layout)

        # row1
        self.file_1 = qtw.QLineEdit('', form, placeholderText="File1")
        btn_file_1 = qtw.QPushButton('Browse')
        btn_file_1.clicked.connect(self.open_file1_dialog)
        layout.addRow(self.file_1, btn_file_1)

        # row2
        self.file_2 = qtw.QLineEdit('', form, placeholderText="File2")
        btn_file_2 = qtw.QPushButton('Browse')
        btn_file_2.clicked.connect(self.open_file2_dialog)
        layout.addRow(self.file_2, btn_file_2)

        # row3
        btn_compare = qtw.QPushButton('Compare')
        btn_compare.clicked.connect(self.compare_file)
        layout.addRow(btn_compare)

        self.delimeter = qtw.QLineEdit('Delimeter')
        self.delimeter.setText('|')
        layout.addRow('Delimeter:', self.delimeter)

        header_check = qtw.QCheckBox("Has Header", self)
        header_check.setChecked(True)
        layout.addRow(header_check)

        # row4
        self.column_list = qtw.QComboBox()
        layout.addRow('Sorted Column:', self.column_list)

        # add toolbar
        toolbar = qtw.QToolBar('main toolbar')
        toolbar.setIconSize(qtc.QSize(16, 16))
        self.addToolBar(toolbar)

        dock.setWidget(form)

    def compare_file(self):
        print('COMPARE...............')

    sort_order = qtc.Qt.SortOrder.AscendingOrder

    def sort_data(self, col_index):
        print('SORT...............', self.csvdata1[0][col_index])
        try:
            #self.table1.header_clicked.emit(col_index)
            self.column_list.setCurrentIndex(col_index)
        except Exception as e:
            print('type(e):', type(e), 'e:', e)
        # try:
        #     self.table2.sortByColumn(col_index, self.sort_order)
        #     if self.sort_order == qtc.Qt.SortOrder.AscendingOrder:
        #         self.sort_order = qtc.Qt.SortOrder.DescendingOrder
        #     else:
        #         self.sort_order = qtc.Qt.SortOrder.AscendingOrder
        #
        # except Exception as e:
        #     print('Something wrong...........', e)

    def create_table_data(self, file_path, table, csvdata):
        print('column count:', len(csvdata[0]));
        table.setColumnCount(len(csvdata[0]))

        print('header:', csvdata[0]);
        table.setHorizontalHeaderLabels(csvdata[0])
        for header in csvdata[0]:
            self.column_list.addItem(header)

        table.setRowCount(len(csvdata) - 1)

        # row = 0
        # for r in csvdata:
        #     #print('row:', row)
        #     col = 0
        #     for c in r:
        #         #print('column: ', col, 'columnData: ', c)
        #         if row != 0:
        #             table.setItem(row - 1, col, qtw.QTableWidgetItem(str(c)))
        #             col += 1
        #     row += 1
        # print(csvData)
        print('column counts: ', len(csvdata[0]))
        print('csvData length: ', len(csvdata))

    def open_file1_dialog(self):
        filename, ok = qtw.QFileDialog.getOpenFileName(
            self,
            "Select a File",
            directory="C:\\Users\\Admin\\Desktop\\csv"
        )
        print('filename: ', filename, ' ok:', ok)
        try:
            if filename:
                path = Path(filename)
                self.file_1.setText(str(path))
                print('path:', str(path), 'delimeter:', self.delimeter.text())
                csvfile = open(str(path))
                print('csvfile:', os.path.normpath('file://' + str(path)))
                pddataframe = p.read_csv(str(path), sep=self.delimeter.text(),encoding='utf-8',header=None,na_filter=False)
                # print('type(csvdata):', type(pddataframe))
                self.csvdata1 = pddataframe.values.tolist()
                # print('csvdata1:', self.csvdata1)
                self.create_table_data(self.file_1.text(), self.table1, self.csvdata1)
        except Exception as e:
            print('Error:', type(e).__name__, e.args)

    def open_file2_dialog(self):
        filename, ok = qtw.QFileDialog.getOpenFileName(
            self,
            "Select a File",
            "D:\\icons\\avatar\\"
        )
        print('filename: ', filename, ' ok:', ok)
        if filename:
            path = Path(filename)
            self.file_2.setText(str(path))

            csvfile = open(str(path))
            csvreader = csv.reader(csvfile, delimiter=self.delimeter.text())
            self.csvdata2 = list(csvreader)

        self.create_table_data(self.file_2.text(), self.table2, self.csvdata2)

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
