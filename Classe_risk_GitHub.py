
from matplotlib import dates as mpl_date
from matplotlib import pyplot as plt 
import yfinance as yf
import seaborn as sns
from math import *
import numpy as np
import datetime
import sys

class Risk:
    def __init__(self,stock,start=datetime.datetime.today()-datetime.timedelta(days=3650),end=datetime.datetime.today()): ### What self is doing is: Every time a method is called he stored permanently for each object
        self.stock = stock
        self.start=start
    def Hist(self):
        return(yf.download(self.stock,self.start)['Adj Close'].ffill())
    def Vol(self,kind,type,window):
        self.kind = kind
        self.type = type
        self.window = window
        if kind == 'hist':
            if window == '':
                if type == 'Dayli':
                    return('{:.2%}'.format(yf.download(self.stock,self.start)['Adj Close'].ffill().pct_change().std()))
                elif type == 'Annual':
                    return('{:.2%}'.format(yf.download(self.stock,self.start)['Adj Close'].ffill().pct_change().std()*sqrt(252)))
                else:
                    return(str('{:.2%}'.format(yf.download(self.stock,self.start)['Adj Close'].ffill().pct_change().std()))+' is the dayli volatility'   )
            elif window != '':
                if type == 'Dayli':
                    return '{:.2%}'.format(((yf.download(self.stock,self.start)['Adj Close'].ffill().pct_change().rolling(window=window).std())).dropna()[-1])
                elif type == 'Annual':
                    return '{:.2%}'.format((yf.download(self.stock,self.start)['Adj Close'].ffill().pct_change().rolling(window=window).std()*sqrt(252)).dropna()[-1])
                else:
                    return(str('{:.2%}'.format(yf.download(self.stock,self.start)['Adj Close'].ffill().pct_change().std()))+' is the dayli volatility'   )       
        else:
            print('We havent made this kind of Volatility')
    def Mean(self,window):
        self.window = window
        if window == '':
            return (yf.download(self.stock,self.start)['Adj Close'].ffill().mean())
        elif window != '':
             return(yf.download(self.stock,self.start)['Adj Close'].ffill().rolling(window=window).mean()).dropna()[-1]
                     
        else:
            print('We havent made this kind of Mean ')
    def Sharpe(self,FreeRate):
        self.FreeRate= FreeRate
        y = yf.download(self.stock,self.start)['Adj Close'].ffill()
        ra=((y/y[0])-1)
        return ((ra[-1]**(252/len(ra)))- FreeRate)/(y.pct_change().std()*sqrt(252))

print(Risk(['BBAS3.SA','BBDC3.SA'],'2022-03-12').Hist())
print(Risk('BBAS3.SA','2022-03-12').Vol('hist','Dayli',30))
print(Risk('BBAS3.SA','2023-01-01').Mean(30))
print(Risk('BBAS3.SA','1900-01-01').Sharpe(0.1365))