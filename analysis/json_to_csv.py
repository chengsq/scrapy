#encoding: utf-8
import pandas as pd
import sys
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pygal
import math
import numpy

from pandas import ExcelWriter


def ReadData(file_name):
    datas = []
    for line in open( file_name).readlines():
        try:
            datas.append(json.loads(line))
        except:
            continue

    return pd.DataFrame(datas)

def UnicodeToUtf8(s):
    return s.encode('utf-8')

def DataMap(df,f,col):
    #for row in rimcol.iteritems:
    for index, row in df.iterrows():
        row[col] = f(row[col])
    return df

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "usage: %s file_name" %sys.argv[0]
    file_name = sys.argv[1]
    df = ReadData(file_name)
    #print df.rows

    print df.columns
    print df.describe()
    print df.head()
    #[['area','chengjiao_date']]
    df = df.drop_duplicates(subset = ['date','area'],keep = 'first')
    df.to_csv(sys.argv[1]+'.csv',encoding='utf-8')
    writer = ExcelWriter(sys.argv[1]+'.xlsx')
    df.to_excel(writer,'Sheet2')
    writer.save()
