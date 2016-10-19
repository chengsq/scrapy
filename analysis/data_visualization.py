#encoding: utf-8
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm


def Stripplot(x_,y_,data_):
    sns.set(style="whitegrid", color_codes=True)
    sns.stripplot(x = x_, y=y_, data = data_, jitter=True);

def PairPlot(df):
    sns.set()
    sns_plot = sns.pairplot(df, hue="target")
    sns_plot.savefig("pairplot.png")

def BarPlot(x_,y_,df):
    sns.set()
    ax = sns.barplot(y="IDATACOMPLETIONSCORES",x='target', data=df)

def CountPlot(y_s,hue_s,df):
    sns.set()
    sns.countplot(y=y_s, hue=hue_s, data=df, palette="Greens_d");

def DistPlot(df):
    sns.set()
    sns.distplot(df,kde = False)

def FactorPlot(index,df):
    sns_plot = sns.factorplot(index, col="deck", col_wrap=4,
      data=df,
      kind="count", size=2.5, aspect=.8)

def JoinPlot(x_,y_,df):
    sns_plot = sns.jointplot(x=x_, y= y_, data=df)
    sns_plot.savefig("joinplot.png")


if __name__ == '__main__':
    data_path = "/Users/shiqing/Workspace/data/maiya-160623/yd_sample_data/maiya_x/"
    file_name = "maya_x_result.csv"

    df = pd.read_csv(data_path + file_name)
    print df.head()
    #BarPlot('','',df)
    #CountPlot('IDATACOMPLETIONSCORES','target',df)
    #DistPlot(df['IDATACOMPLETIONSCORES'])
    #FactorPlot('IDATACOMPLETIONSCORES',)
    #JoinPlot('IDATACOMPLETIONSCORES','target',df)
    PairPlot(df)
    plt.show()
