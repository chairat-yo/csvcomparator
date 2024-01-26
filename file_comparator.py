import os.path
import sys
import csv
import time
import difflib as dl
import pandas as p
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg
from pathlib import Path


class MainWindow(qtw.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('File Comparator')
        self.setWindowIcon(qtg.QIcon('./assets/usergroup.png'))
        self.setGeometry(100, 100, 1080, 600)

        table_layout = qtw.QHBoxLayout()
        self.central_widget = qtw.QWidget(self)
        self.central_widget.setLayout(table_layout)
        self.setCentralWidget(self.central_widget)

        # Result Text Edit
        self.result_text = qtw.QPlainTextEdit()
        font = self.result_text.font()
        # font.setFamily("Courier")
        font.setPointSize(8)
        self.result_text.setFont(font)
        self.result_text.setLineWrapMode(qtw.QPlainTextEdit.LineWrapMode.NoWrap)
        # self.textedit1.setLineWrapMode(qtw.QTextEdit.LineWrapMode.FixedPixelWidth)
        self.result_text.setTabStopDistance(4)
        table_layout.addWidget(self.result_text)

        dock = qtw.QDockWidget('Files to Compare')
        dock.setFeatures(qtw.QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.addDockWidget(qtc.Qt.DockWidgetArea.RightDockWidgetArea, dock)

        ##############################################
        #################create form##################
        ##############################################
        form = qtw.QWidget()
        form.setMinimumWidth(300)
        layout = qtw.QFormLayout(form)
        form.setLayout(layout)

        # row1
        self.file_1 = qtw.QLineEdit('', form, placeholderText="File1")
        self.file_1.setMinimumWidth(300)
        btn_file_1 = qtw.QPushButton('Browse')
        btn_file_1.clicked.connect(self.open_file1_dialog)
        layout.addRow(self.file_1, btn_file_1)

        # row2
        self.file_2 = qtw.QLineEdit('', form, placeholderText="File2")
        self.file_2.setMinimumWidth(300)
        btn_file_2 = qtw.QPushButton('Browse')
        btn_file_2.clicked.connect(self.open_file2_dialog)
        layout.addRow(self.file_2, btn_file_2)

        # row3
        btn_compare = qtw.QPushButton('Compare')
        btn_compare.clicked.connect(self.compare_file)
        layout.addRow(btn_compare)

        sort_enable = qtw.QCheckBox("Sort", self)
        sort_enable.setChecked(True)
        layout.addRow(sort_enable)

        # add toolbar
        toolbar = qtw.QToolBar('main toolbar')
        toolbar.setIconSize(qtc.QSize(16, 16))
        self.addToolBar(toolbar)

        dock.setWidget(form)

    def compare_file(self):
        with open(self.file_1.text(), 'r') as file1:
            file1_contents = file1.readlines()
        with open(self.file_2.text(), 'r') as file2:
            file2_contents = file2.readlines()

        file1_contents.sort()
        # for i in range(len(file1_contents)):
        #     print(file1_contents[i])

        print('-----------------------')
        file2_contents.sort()
        # for i in range(len(file2_contents)):
        #     print(file2_contents[i])

        diff = dl.unified_diff(
            file1_contents, file2_contents)
        # diff = dl.unified_diff(
        #     file1_contents, file2_contents, fromfile="file1.txt",
        #     tofile="file2.txt", lineterm='')

        print('file1:', type(file1), 'diff:', type(diff))

        for line in diff:
            self.result_text.appendPlainText(line)
            # print(line)
    def sort_data(self, col_index):
        print('SORT...............',)
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


    def getCSVHeader(self, filename, delimeter):
        try:
            if filename:
                header_row = p.read_csv(str(filename), sep=delimeter, nrows=1)
                print('header_row:', header_row)
                header_list = list(map(str, header_row.values.tolist()[0]))
                print('header_list',header_list)
                self.header_list.addItems(header_list)
        except Exception as e:
            print('Exception:', type(e), e)

    # def compare_csv(self):
    #     from csv_diff import load_csv, compare
    #     diff = compare(
    #         load_csv(open("one.csv"), key="id"),
    #         load_csv(open("two.csv"), key="id")
    #     )

    def open_file1_dialog(self):
        self.filename1, ok = qtw.QFileDialog.getOpenFileName(
            self,
            "Select a File",
            directory="C:\\Users\\Admin\\Desktop\\csv"
        )
        self.file_1.setText(self.filename1)

    def open_file2_dialog(self):
        self.filename2, ok = qtw.QFileDialog.getOpenFileName(
            self,
            "Select a File",
            "D:\\icons\\avatar\\"
        )
        self.file_2.setText(self.filename2)


# class Worker(qtc.QThread):
#     create_rows = qtc.pyqtSignal(list, qtw.QWidget)
#
#     def __init__(self, df: pandas.DataFrame, textedit: qtw.QTextEdit):
#         super(Worker, self).__init__()
#         self.df = df
#         self.textedit = textedit
#
#     def run(self):
#         """Long-running task."""
#         n = 5000
#         self.list_df = [self.df[i:i + n] for i in range(1, len(self.df) - 1, n)]
#         print('list_df(chucks):', len(self.list_df))
#         try:
#             for index in range(len(self.list_df)):
#                 ddf = self.list_df[index].astype(str).values
#                 # self.create_table_data(self.textedit, ddf)
#                 self.create_rows.emit(ddf, self.textedit)
#                 time.sleep(2)
#                 # time.sleep(10)
#             # self.finished.emit()
#         except Exception as e:
#             print('Loop Error:', type(e), e)
#
#         print('total rows:', len(self.df))

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
