import os.path
import sys
import csv
import pandas as p
from pathlib import Path
from csv_diff import load_csv, compare
class CmdCSVComparator:

    def __init__(self, *args, **kwargs):
        self.file1 = input('File 1:')
        self.delimeter = input('Delimeter:')
        self.sorted_col = input('Sorted Column:')

        print('File1:', self.file1)
        print('Delimeter:', self.delimeter)
        print('Sorted Column:', self.sorted_col)

        csvdata1 = self.loadCSV(self.file1, self.sorted_col,self.delimeter)
        print('csvdata1:', csvdata1)

    def loadCSV(self, filename, sorted_col, delimeter):
        if filename:
            pddataframe = p.read_csv(str(filename), sep=delimeter, encoding='utf-8', header=None,
                                     na_filter=False)
            pddataframe.sort_values(pddataframe.columns[0], ascending=True,inplace=True)
            print('pddataframe:', pddataframe)
            return pddataframe.values.tolist()

if __name__ == '__main__':
    CmdCSVComparator(sys.argv)
