
from matplotlib import dates as mpl_date
from matplotlib import pyplot as plt 
import yfinance as yf
import seaborn as sns
import pandas as pd
from math import *
import numpy as np
import datetime
import sys

# p=yf.download('BBAS3.SA',start=datetime.datetime.today()-datetime.timedelta(days=3650))['Adj Close'].dropna()
# p=pd.DataFrame(p)
# p['Log return']=((p['Adj Close']/p['Adj Close'].shift(1))).apply(log)

# print(p)
# sys.exit()
class Risk:
    def __init__(self,stock,start=datetime.datetime.today()-datetime.timedelta(days=3650), end=datetime.datetime.today()): ### What self is doing is: Every time a method is called he stored permanently for each object
        self.stock = stock
        self.start=start
        self.end= end
    def Hist(self):
        return(yf.download(self.stock,self.start)['Adj Close'].dropna())
    def Return(self):
        return  self.Hist().pct_change().dropna()
    def Vol(self,kind='hist',type='Dayli',window='',Lambda=0.94):
        self.kind = kind
        self.type = type
        self.window = window
        self.Lambda = Lambda
        if kind == 'hist':
            if window == '':
                if type == 'Dayli':
                    return('{:.2%}'.format(self.Return().std()))
                elif type == 'Weekly':
                    return('{:.2%}'.format(self.Return().std()*sqrt(5)))                
                elif type == 'Monthly':
                    return('{:.2%}'.format(self.Return().std()*sqrt(20))) 
                elif type == 'Annual':
                    return('{:.2%}'.format(self.Return().std()*sqrt(252)))
                else:
                    return(str('{:.2%}'.format(self.Return().std()))+' is the dayli volatility'   )
            elif window != '':
                if type == 'Dayli':
                    return '{:.2%}'.format(((self.Return().rolling(window=window).std())).dropna()[-1])
                elif type == 'Weekly':
                    return '{:.2%}'.format((self.Return().rolling(window=window).std()*sqrt(5)).dropna()[-1])
                elif type == 'Monthly':
                    return '{:.2%}'.format((self.Return().rolling(window=window).std()*sqrt(20)).dropna()[-1])                
                elif type == 'Annual':
                    return '{:.2%}'.format((self.Return().rolling(window=window).std()*sqrt(252)).dropna()[-1])
                else:
                    return(str('{:.2%}'.format(self.Return().std()))+' is the dayli volatility'   )       
        elif kind == 'EWMA':
            if window == '':
                if type == 'Dayli':            
                    p=self.Hist()
                    p=pd.DataFrame(p)
                    p['Log return']=((p['Adj Close']/p['Adj Close'].shift(1))).apply(log)
                    N=len(p['Adj Close'])            
                    M=len(p['Log return'])
                    u=p['Log return'].mean()  
                    p['∑']=p['Log return']-u
                    for j in range(len(p['∑'])):
                        if j <= 0:
                            p['∑'][j]=0
                        else:
                            p['∑'][j]=pow((p['Log return'][j] - u),2)
                            # p['∑'][j]=pow((p['∑'][j]),2)
                    Vol=sqrt((1/(M-1))*(p['∑'].sum())) ### Volatility is the square root of variance
                    Vn_1=p['Log return'][:-1].std()    ### Volatility of n-1!                                      ^     
                    var1=Vn_1**2 ### Variance of n-1!        |
                    u2=pow(p['Log return'][-2],2) ### Power of the penultimate return
                    V_EWMA = sqrt((Lambda*var1) + (1-Lambda)*u2)
                    return '{:.2%}'.format(V_EWMA)
                
                if type == 'Weekly': 
                    p=self.Hist()
                    p=pd.DataFrame(p)
                    p['Log return']=((p['Adj Close']/p['Adj Close'].shift(1))).apply(log)
                    N=len(p['Adj Close'])            
                    M=len(p['Log return'])
                    u=p['Log return'].mean()  
                    p['∑']=p['Log return']-u
                    for j in range(len(p['∑'])):
                        if j <= 0:
                            p['∑'][j]=0
                        else:
                            p['∑'][j]=pow((p['Log return'][j] - u),2)
                            # p['∑'][j]=pow((p['∑'][j]),2)
                    Vol=sqrt((1/(M-1))*(p['∑'].sum())) ### Volatility is the square root of variance
                    Vn_1=p['Log return'][:-1].std()    ### Volatility of n-1!                                      ^     
                    var1=Vn_1**2 ### Variance of n-1!        |
                    u2=pow(p['Log return'][-2],2) ### Power of the penultimate return
                    V_EWMA = sqrt((Lambda*var1) + (1-Lambda)*u2)*sqrt(5)
                    return '{:.2%}'.format(V_EWMA)
                
                if type == 'Monthly': 
                    p=self.Hist()
                    p=pd.DataFrame(p)
                    p['Log return']=((p['Adj Close']/p['Adj Close'].shift(1))).apply(log)
                    N=len(p['Adj Close'])            
                    M=len(p['Log return'])
                    u=p['Log return'].mean()  
                    p['∑']=p['Log return']-u
                    for j in range(len(p['∑'])):
                        if j <= 0:
                            p['∑'][j]=0
                        else:
                            p['∑'][j]=pow((p['Log return'][j] - u),2)
                            # p['∑'][j]=pow((p['∑'][j]),2)
                    Vol=sqrt((1/(M-1))*(p['∑'].sum())) ### Volatility is the square root of variance
                    Vn_1=p['Log return'][:-1].std()    ### Volatility of n-1!                                      ^     
                    var1=Vn_1**2 ### Variance of n-1!        |
                    u2=pow(p['Log return'][-2],2) ### Power of the penultimate return
                    V_EWMA = sqrt((Lambda*var1) + (1-Lambda)*u2)*sqrt(20)
                    return '{:.2%}'.format(V_EWMA)
                
                if type == 'Annual': 
                    p=self.Hist()
                    p=pd.DataFrame(p)
                    p['Log return']=((p['Adj Close']/p['Adj Close'].shift(1))).apply(log)
                    N=len(p['Adj Close'])            
                    M=len(p['Log return'])
                    u=p['Log return'].mean()  
                    p['∑']=p['Log return']-u
                    for j in range(len(p['∑'])):
                        if j <= 0:
                            p['∑'][j]=0
                        else:
                            p['∑'][j]=pow((p['Log return'][j] - u),2)
                            # p['∑'][j]=pow((p['∑'][j]),2)
                    Vol=sqrt((1/(M-1))*(p['∑'].sum())) ### Volatility is the square root of variance
                    Vn_1=p['Log return'][:-1].std()    ### Volatility of n-1!                                      ^     
                    var1=Vn_1**2 ### Variance of n-1!        |
                    u2=pow(p['Log return'][-2],2) ### Power of the penultimate return
                    V_EWMA = sqrt((Lambda*var1) + (1-Lambda)*u2)*sqrt(252)
                    return '{:.2%}'.format(V_EWMA)               
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
print(Risk('BBAS3.SA','2022-03-12').Vol('hist','Annual'))
print(Risk('BBAS3.SA').Vol(kind='EWMA',type='Annual'))
print(Risk('BBAS3.SA','2023-01-01').Mean('return'))
print(Risk('BBAS3.SA','1900-01-01').Sharpe())
print(Risk('BRL=X','2023-01-01').VaR())
