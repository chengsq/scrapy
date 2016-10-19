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


def ReadData(file_name):
    datas = []
    for line in open( file_name).readlines():
        try:
            datas.append(json.loads(line))
        except:
            continue

    return pd.DataFrame(datas)

def get_unit_price_count(df):
    kd = df.value_counts()
    pie_chart = pygal.Pie()
    pie_chart.title = u'单价分布'
    for ind, num in kd.iteritems():
        pie_chart.add("%s:%s" % (ind, num), num)
    pie_chart.render_to_file(os.path.dirname(__file__) + 'chart/unit_price_count.svg')


def get_total_price_count(df):
    kd = df.value_counts()
    pie_chart = pygal.Pie()
    pie_chart.title = u'总价分布'
    for ind, num in kd.iteritems():
        pie_chart.add("%s:%s" % (ind, num), num)
    pie_chart.render_to_file(os.path.dirname(__file__) + 'chart/total_price.svg')



if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "usage: %s file_name" %sys.argv[0]
    file_name = sys.argv[1]
    df = ReadData(file_name)
    df[['total_price','unit_price']] = df[['total_price','unit_price']].apply(pd.to_numeric)
    print df.columns
    print df.describe()
    aa = (numpy.asarray(df.total_price))
    df.total_price = numpy.around(aa /40) * 40
    get_total_price_count(df.total_price)

    aa = (numpy.asarray(df.unit_price))
    df.unit_price = numpy.around(aa /3000) * 3000
    #get_total_price_count(df.unit_price)
    get_unit_price_count(df.unit_price)
    #sns.set()
    #sns.distplot(df.describe(), kde=False)
    #plt.show()
