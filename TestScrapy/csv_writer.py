import  pandas as pd
import os
import csv

basedir = os.path.dirname(os.path.dirname(__file__))
class CSVWriter():
    def __init__(self,fieldnames):
        with open(basedir + '/data.csv', 'w') as csvfile:
            self.flag = 0
            self.writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            self.writer.writeheader()

    def writeDict(self,d):
        self.writer.writerow(d)
