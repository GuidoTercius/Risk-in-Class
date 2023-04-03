
from matplotlib import dates as mpl_date
from matplotlib import pyplot as plt 
import yfinance as yf
import seaborn as sns
from math import *
import numpy as np
import datetime
import sys

class Risk:
    def __init__(self,stock,start='1900-01-01', end=datetime.today()): ### What self is doing is: Every time a method is called he stored permanently for each object
        self.stock = stock
        self.start=start
        self.end= end
    def Hist(self):
        return(yf.download(self.stock,self.start)['Adj Close'].dropna())
    def Return(self):
        return  self.Hist().pct_change().dropna()
    def Vol(self,kind='hist',type='Dayli',window=''):
        self.kind = kind
        self.type = type
        self.window = window
        if kind == 'hist':
            if window == '':
                if type == 'Dayli':
                    return('{:.2%}'.format(self.Return().std()))
                elif type == 'Weekly':
                    return('{:.2%}'.format(self.Return().std()*sqrt(5)))                
                elif type == 'Annual':
                    return('{:.2%}'.format(self.Return().std()*sqrt(252)))
                else:
                    return(str('{:.2%}'.format(self.Return().std()))+' is the dayli volatility'   )
            elif window != '':
                if type == 'Dayli':
                    return '{:.2%}'.format(((self.Return().rolling(window=window).std())).dropna()[-1])
                elif type == 'Annual':
                    return '{:.2%}'.format((self.Return().rolling(window=window).std()*sqrt(252)).dropna()[-1])
                else:
                    return(str('{:.2%}'.format(self.Return().std()))+' is the dayli volatility'   )       
        else:
            print('We havent made this kind of Volatility')
    def Mean(self,element='Price',window=''):
        self.window = window
        self.element = element
        if element == 'return':
            if window == '':
                return '{:.2%}'.format(self.Return().mean())
            elif window != '':
                return'{:.2%}'.format((self.Return().rolling(window=window).mean()).dropna()[-1])
                        
            else:
                print('We havent made this kind of Mean ')
        elif element== 'Price':
            if window == '':
                return (self.Hist().mean())
            elif window != '':
                return(self.Hist().rolling(window=window).mean()).dropna()[-1]
                        
            else:
                print('We havent made this kind of Mean ')                
        else:
            print('We havent made this kind of Mean ')           
    def Sharpe(self,FreeRate=0.1365):
        self.FreeRate= FreeRate
        y = self.Hist()
        ra=((y/y[0])-1)
        return ((ra[-1]**(252/len(ra)))- FreeRate)/(y.pct_change().std()*sqrt(252))
    def VaR(self,probability=0.05):
        self.probabilty=probability
        return '{:.2%}'.format(np.quantile(self.Return(),probability))
print(Risk(['BBAS3.SA','BBDC3.SA'],'2022-03-12').Hist())
print(Risk(['BBAS3.SA','BBDC3.SA'],'2022-03-12').Return())
print(Risk('BBAS3.SA','2022-03-12').Vol('hist','Dayli',30))
print(Risk('BBAS3.SA','2023-01-01').Mean('return'))
print(Risk('BBAS3.SA','1900-01-01').Sharpe())
print(Risk('BRL=X','2023-01-01').VaR())