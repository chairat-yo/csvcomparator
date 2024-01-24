import os.path
import sys
import csv
import time

import pandas
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

        # csv text table1
        self.textedit1 = qtw.QPlainTextEdit()
        font = self.textedit1.font()
        # font.setFamily("Courier")
        font.setPointSize(8)
        self.textedit1.setFont(font)
        self.textedit1.setLineWrapMode(qtw.QPlainTextEdit.LineWrapMode.NoWrap)
        # self.textedit1.setLineWrapMode(qtw.QTextEdit.LineWrapMode.FixedPixelWidth)
        self.textedit1.setTabStopDistance(4)
        table_layout.addWidget(self.textedit1)

        # csv text table2
        self.textedit2 = qtw.QTextEdit(lineWrapMode=qtw.QTextEdit.LineWrapMode.NoWrap)
        table_layout.addWidget(self.textedit2)

        # scroll
        self.textedit1.verticalScrollBar().valueChanged.connect(self.textedit2.verticalScrollBar().setValue)
        self.textedit2.verticalScrollBar().valueChanged.connect(self.textedit1.verticalScrollBar().setValue)

        self.textedit1.horizontalScrollBar().valueChanged.connect(self.textedit2.horizontalScrollBar().setValue)
        self.textedit2.horizontalScrollBar().valueChanged.connect(self.textedit1.horizontalScrollBar().setValue)


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



    def loadCSV(self, filename, sorted_col, delimeter, textwidget: qtw.QPlainTextEdit):
        if filename:
            pddataframe = p.read_csv(str(filename), sep=delimeter, encoding='utf-8', header=None, na_filter=False)
            print('Successfully load....')
            headers = pddataframe.values.tolist()[0]
            print('header:', headers)
            print('column count:', len(headers))
            print('Successfully header....')

            alldata = pddataframe.values.tolist()
            print('before del:', len(alldata))
            del alldata[0]
            print('after del:', len(alldata))
            # pddataframe.sort_values(pddataframe.columns[sorted_col], ascending=True,inplace=True)
            # print('Successfully sort....')
            # print('type():', type(pddataframe.to_string()))
            # split DataFrame into chunks

            # Step 2: Create a QThread object
            self.worker_thread = qtc.QThread()
            # Step 3: Create a worker object
            self.worker = Worker(pddataframe, textwidget)
            self.worker.create_rows.connect(self.create_row_text)
            # Step 4: Move worker to the thread
            self.worker.moveToThread(self.worker_thread)
            # Step 5: Connect signals and slots
            self.worker_thread.started.connect(self.worker.run)
            # Step 6: Start the thread
            self.worker_thread.start()

    def create_row_text(self, chunkdata, textedit: qtw.QPlainTextEdit):
        #print('create row text:', chunkdata)
        # row = textedit.rowCount()
        # print('rowcount:', row, 'rowdata:', rowdata)

        try:

            # chunk_str = ''
            for rowdata in chunkdata:
                # print('create row:', rowdata)
                chunk_str = '\t'.join(rowdata)
                textedit.appendPlainText(chunk_str)
            #     for c in r:
            #         chunk_str = c + '\t' + chunk_str
                # for c in r:
                #     chunk_str = join()
            # textedit.appendPlainText(chunk_str)

                # print('create row:', row)
                # for c in r:
                #     textedit.insertPlainText(c)
                #     textedit.insertPlainText('\t')
                # textedit.appendPlainText('')
                # row += 1
        # textedit.insertPlainText('a')
        # print('a')

        except BaseException as e:
            print('Error Creating Text:', type(e), e)
    def open_file1_dialog(self):
        filename, ok = qtw.QFileDialog.getOpenFileName(
            self,
            "Select a File",
            directory="C:\\Users\\Admin\\Desktop\\csv"
        )
        print('filename: ', filename, ' ok:', ok)
        try:
            if filename:
                self.loadCSV(filename,0,self.delimeter.text(), self.textedit1)
                # path = Path(filename)
                # self.file_1.setText(str(path))
                # print('path:', str(path), 'delimeter:', self.delimeter.text())
                # csvfile = open(str(path))
                # print('csvfile:', os.path.normpath('file://' + str(path)))
                # pddataframe = p.read_csv(str(path), sep=self.delimeter.text(),encoding='utf-8',header=None,na_filter=False)
                # # print('type(csvdata):', type(pddataframe))
                # self.csvdata1 = pddataframe.values.tolist()
                # # print('csvdata1:', self.csvdata1)
                # self.create_table_data(self.file_1.text(), self.table1, self.csvdata1)
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


class Worker(qtc.QThread):
    create_rows = qtc.pyqtSignal(list, qtw.QWidget)

    def __init__(self, df: pandas.DataFrame, textedit: qtw.QTextEdit):
        super(Worker, self).__init__()
        self.df = df
        self.textedit = textedit

    def run(self):
        """Long-running task."""
        n = 5000
        self.list_df = [self.df[i:i + n] for i in range(1, len(self.df) - 1, n)]
        print('list_df(chucks):', len(self.list_df))
        try:
            for index in range(len(self.list_df)):
                # print("Start Chunk", index, 'type(chunk):', type(self.list_df[index]), 'dir', dir(self.list_df[index]))
                ddf = self.list_df[index].astype(str).values
                # self.create_table_data(self.textedit, ddf)
                self.create_rows.emit(ddf, self.textedit)
                time.sleep(2)
                # time.sleep(10)
            # self.finished.emit()
        except Exception as e:
            print('Loop Error:', type(e), e)

        print('total rows:', len(self.df))

    # def create_table_data(self, textedit, chunkdata):
    #     try:
    #         self.create_rows.emit(chunkdata, textedit)
    #     except Exception as e:
    #         print('Error when creating table:', type(e), e)
        # print('column counts: ', len(csvdata[0]))
        # print('/csvData length: ', len(csvdata))

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
