def twodigit(n):  # 講數值轉為二位數字串
    if (n < 10):
        retstr = '0' + str(n)
    else:
        retstr = str(n)
    return retstr


def convertDate(date):
    strl = str(date)
    yearstr = strl[:3]  # 取出民國年
    realyear = str(int(yearstr) + 1911)  # 轉為西元年
    realdate = realyear + strl[4:6] + strl[7:9]  # 組合日期
    return realdate


import requests
import json, csv
import pandas as pd
import os
import time
import matplotlib.pyplot as plt
import datetime
import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np

pd.options.mode.chained_assignment = None

StockIDs = ['00673R','00672L','00642U'] #股票ID
for StockID in StockIDs:
    for datetime in range(2017,2020):
        urlbase = 'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date='  # 網址前半
        urltail = '10&stockNo='  # 網址後半
        filepath = StockID + '.csv'
        for i in range(1, 13):  # 取1到12數字
            url_twse = urlbase + str(datetime) + twodigit(i) + urltail + StockID  # 組合網址
            res = requests.get(url_twse)
            jdata = json.loads(res.text)
            outputfile = open(filepath, 'a', newline='', encoding='utf-8-sig')
            outputwriter = csv.writer(outputfile)
            if i == 1 and datetime == 2017:
                outputwriter.writerow(jdata['fields'])
            if 'data' is not None:
                for dataline in (jdata.setdefault('data','')):
                    outputwriter.writerow(dataline)
            time.sleep(5)
     outputfile.close()


price_ = []
for Stockdraw in StockIDs:
    filepath = Stockdraw + '.csv'
    pdStockdraw = pd.read_csv(filepath,header=0, encoding='utf-8-sig')
    pdStockdraw.insert(0,column ="StockID",value = Stockdraw)
    price_.append(pdStockdraw)
for i in range(len(pdStockdraw['日期'])):
    pdStockdraw['日期'][i] = convertDate(pdStockdraw['日期'][i])
pdStockdraw['日期'] = pd.to_datetime(pdStockdraw['日期'])

#calculate bias#
OilBias = []
for x in range(1,len(StockIDs)):
    Bias = []
    for i in range(len(pdStockdraw['收盤價'])):
        delt = round((price_[x]['收盤價'][i]) - (price_[0]['收盤價'][i]),2)
        Bias.append(delt)
    OilBias.append(Bias)


figure = make_subplots(specs=[[{"secondary_y": True}]])
a = 0
for y in range(0,len(StockIDs)):
    co1 = ['black', 'red', 'skyblue', 'olive', 'megreen']
    figure.add_trace(
        go.Scatter(x=price_[0]['日期'], y=price_[y]['收盤價'], name=price_[y]['StockID'][0], mode="lines", fillcolor= co1[a]),secondary_y=False)
    a += 1

for yy in range(0,(len(StockIDs))-1):
    figure.add_trace(go.Scatter(x=price_[0]['日期'], y=OilBias[yy],name = StockIDs[yy+1]+'-'+StockIDs[0], mode="markers",marker=dict(size = 3.5)), secondary_y=True)
figure.update_yaxes(range=[0,40],rangemode='tozero',showgrid=True,showticklabels=True,zeroline=True, secondary_y=False)
figure.update_yaxes(range=[-30,30],rangemode='tozero',showgrid=True,showticklabels=True,zeroline=True, secondary_y=True)
plotly.offline.plot(figure)

