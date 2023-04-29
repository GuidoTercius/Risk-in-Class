from matplotlib import dates as mpl_date
from matplotlib import pyplot as plt 
import yfinance as yf
import seaborn as sns
import pandas as pd
from math import *
import numpy as np
import datetime
import sys

class Risk:
    def __init__(self,stock='',start=datetime.datetime.today()-datetime.timedelta(days=3650), end=datetime.datetime.today()): ### What self is doing is: Every time a method is called he stored permanently for each object
        self.stock = stock
        self.start=start
        self.end= end
    def Hist(self):
        return(yf.download(self.stock,self.start)['Adj Close'].dropna())
    def Return(self):
        return  self.Hist().pct_change().dropna()
    def Vol(self,kind='hist',type='Daily',window='',Lambda=0.94):
        self.kind = kind
        self.type = type
        self.window = window
        self.Lambda = Lambda
        if kind == 'hist':
            if window == '':
                if type == 'Daily':
                    return('{:.2%}'.format(self.Return().std()))
                elif type == 'Weekly':
                    return('{:.2%}'.format(self.Return().std()*sqrt(5)))                
                elif type == 'Monthly':
                    return('{:.2%}'.format(self.Return().std()*sqrt(20))) 
                elif type == 'Annual':
                    return('{:.2%}'.format(self.Return().std()*sqrt(252)))
                else:
                    return(str('{:.2%}'.format(self.Return().std()))+' is the daily volatility'   )
            elif window != '':
                if type == 'Daily':
                    return ((self.Return().rolling(window=window).std())).dropna()
                elif type == 'Weekly':
                    return (self.Return().rolling(window=window).std()*sqrt(5)).dropna()
                elif type == 'Monthly':
                    return (self.Return().rolling(window=window).std()*sqrt(20)).dropna()              
                elif type == 'Annual':
                    return (self.Return().rolling(window=window).std()*sqrt(252)).dropna()
                else:
                    return(str('{:.2%}'.format(self.Return().std()))+' is the Daily volatility'   )       
        elif kind == 'EWMA':
            if window == '':        
                    p=self.Hist()
                    p=pd.DataFrame(p)
                    p['Log return']=((p['Adj Close']/p['Adj Close'].shift(1))).apply(log)
                    p['Vol EWMA'] = np.nan
                    for a in range(1,len(p['Adj Close'])):
                        if a == 1: 
                            p['Vol EWMA'][a]=0
                        elif a == 2:  
                            var1=(p['Log return'][0:a+1].std())**2  ### The power of std of Log return 0 to now ###  Variance of n!  
                            u2=pow(p['Log return'][a],2)            ### The 
                            p['Vol EWMA'][a] = sqrt((Lambda*var1) + (1-Lambda)*u2) 
                        
                        else:
                            var1=(p['Vol EWMA'][(a-1)])**2 ### Variance of n-1!  
                            u2=pow(p['Log return'][a-1],2)
                            p['Vol EWMA'][a] = sqrt((Lambda*var1) + (1-Lambda)*u2)
                    V_EWMA = p['Vol EWMA']
            if self.type == 'Daily':    
                return (V_EWMA)
                
            elif type == 'Weekly': 
                return (V_EWMA*sqrt(5))
                
            elif type == 'Monthly': 
                return (V_EWMA*sqrt(20))
                
            elif type == 'Annual': 
                return (V_EWMA*sqrt(252))
            
        elif kind == 'Garch':
            p=self.Hist()
            p=pd.DataFrame(p)
            p['plog']=(p['Adj Close']/p['Adj Close'].shift(1)).apply(log).dropna() ### return by log
            u=p['plog'].mean() ### average of return by log
            p['Vari']=np.nan
            for j in range(len(p['plog'])):     
                p['Vari'][j]=pow(p['plog'][j]-(p['plog'][0:(j+1)].mean()),2)    ### Calculating the Variance from D0 to D(i-n)
            Vl=(p['Vari'].sum())/(len(p['Vari'])-1) ### long-run average variance rate, VL 
            a=0.15 ### alpha ; Is the weight assigned to the power of the last return
            l=0.80 ### Lambda ; Is the weight assigned to the standard deviation of n-1
            g=1-(l+a) ### the sum of Lambda, alpha and g is = 1 ; g is the weight assigned to the VL ("long-run average variance rate")
            o=g*Vl    ### The Vl ponderate

            u2 =p['plog'][-1]**2 ### the last return square

            Varn_1=pow(p['plog'][:-1].std(),2) #Var of n-1
            Vol_Garch= sqrt((o)+(Varn_1*l)+(u2*a)) # the sqrt(sum of all variables ponderate) == Vol Garch
            if self.type == 'Daily':    
                return (Vol_Garch)
                
            elif type == 'Weekly': 
                return (Vol_Garch*sqrt(5))
                
            elif type == 'Monthly': 
                return (Vol_Garch*sqrt(20))
                
            elif type == 'Annual': 
                return (Vol_Garch*sqrt(252))
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
    def MDD(self,kind='History'):
        self.kind= kind
        h=self.Hist()
        MDD=(h/h.cummax())-1
        if kind == 'History':
            return MDD
        elif kind == 'Min':
            return MDD.min()
    def graph(self,obj,titre="",yl="",xl='Date'):
        
        self.obj=obj
        self.titre=titre
        self.xl=xl
        self.yl=yl
        plt.plot(obj)
        plt.title(titre)
        plt.gcf().autofmt_xdate()
        plt.xlabel(xl)
        plt.ylabel(yl)
        plt.show()