import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import inspect
from typing import Callable as function

index_data = pd.read_csv('data.csv')

class DataSet:
    def __init__(self, data: pd.DataFrame, label: str, color: str):
        self.data = data
        self.label = label
        self.color = color

   

def displayMain(*datasets: DataSet,label: str,start_date=0, end_date=564) -> None: 
    
    for dataset in datasets:
        plt.plot(dataset.data.iloc[start_date:end_date,1], color=dataset.color, label=dataset.label)
    


    plt.xlabel('Year')
    l = list(range(start_date,end_date,60))
    for i in range(len(l)):
        year = l[i] // 12 + 1979
        l[i] = str(year)
    plt.xticks(ticks=range(start_date,end_date,60), labels=l)
    plt.ylabel('Value')
    plt.title(label)
    formatter = ticker.ScalarFormatter()
    formatter.set_scientific(False)
    plt.gca().yaxis.set_major_formatter(formatter)

    plt.legend()
    plt.show()

def data_mntl(index: pd.DataFrame, mntl: int) -> np.ndarray:

    fracs = np.zeros(len(index))
    fracs[0] = mntl / index.iloc[0,1]
    portfolio = np.zeros(len(index))
    portfolio[0] = fracs[0] * index.iloc[0,1]
    for i in range(1, len(index)):

       fracs[i] = fracs[i-1] + (mntl / index.iloc[i,1] ) 
       portfolio[i] = fracs[i] * index.iloc[i,1]
    DataReturn = pd.DataFrame({'MONTH': index.iloc[:,0], 'MSCI World': portfolio})

    DataReturn.to_csv(str(inspect.currentframe().f_code.co_name) + '.csv')
    return DataReturn

def data_strat1(index: pd.DataFrame, mntl: int, _testResession: function, _invFrac: float) -> np.ndarray:
    fedfunds = pd.read_csv('fedfunds.csv')
    #man investiert teil in fedfunds cash wenn kein resession
    investfrac = _invFrac
    cashfrac = 1 - investfrac
    
    fracs = np.zeros(len(index))
    fracs[0] = mntl / index.iloc[0,1]
    portfolio = np.zeros(len(index))
    portfolio[0] = fracs[0] * index.iloc[0,1]
    cashreserve = 0
    cashvalue = np.zeros(len(index))
    resession = False
    for i in range(1, len(index)):
        #check for resession
        if _testResession:
            resession = True
        else:
            resession = False
        if resession:
            cashreserve += mntl #Alles in cash weil sofort invest
            fracs[i] = fracs[i-1] + (cashreserve / index.iloc[i,1] ) 
            portfolio[i] = fracs[i] * index.iloc[i,1]
            cashreserve = 0
        else:
            cashreserve += mntl * cashfrac
            fracs[i] = fracs[i-1] + ((mntl*investfrac) / index.iloc[i,1] ) 
            portfolio[i] = fracs[i] * index.iloc[i,1]
        cashreserve = cashreserve * (1 + fedfunds.iloc[i,1]/1200) #monthly interest
        cashvalue[i] = cashreserve
        
    DataReturn = pd.DataFrame({'MONTH': index.iloc[:,0], 'MSCI World': portfolio})#, 'Cash Value': cashvalue})
    
    DataReturn.to_csv(str(inspect.currentframe().f_code.co_name) + '.csv')
    return DataReturn


def unemResession(i) -> bool:
    global index_data
    index: pd.DataFrame = index_data.copy()
    before = 3
    
    if i > before: return False
    return index.iloc[i,1] < index.iloc[i-before,1]

def testForHighest(strat: function) -> float:
    global index_data
    index: pd.DataFrame = index_data.copy()
    
    for x in range(100):
        values = strat(index=index, mntl=200, _testResession=unemResession, _invFrac=x/1000)["MSCI World"]
        index.insert(loc = x+2, column="STRAT1-"+str(x/100), value=values)
    
    index.to_csv("file.csv")

    return (x)


if __name__ == "__main__":

    invest = 200


    a = testForHighest(data_strat1)
    df_mntl = data_mntl(pd.read_csv('data.csv'), invest)
    ds_mntl = DataSet(df_mntl, 'Portfolio Value Mntl', 'blue')
    
    df_noInvest = pd.DataFrame(
        {'MONTH': df_mntl['MONTH'], 
         'VALUE': list(range(invest,(len(df_mntl)+1)*invest,invest))})
    ds_noInvest = DataSet(df_noInvest, color='red', label='Invested Amount')
    
    df_strat1 = data_strat1(pd.read_csv('data.csv'), invest, unemResession, 0.1)
    ds_strat1 = DataSet(df_strat1, 'Portfolio Value Strat1', 'green')
    
    df_unem = pd.read_csv('unem.csv')
    ds_unem = DataSet(df_unem, 'Unemployment', 'violet')
    
    displayMain(ds_mntl, ds_noInvest, ds_strat1, ds_unem, label='Monthly 200$ in MSCI World Index')
    