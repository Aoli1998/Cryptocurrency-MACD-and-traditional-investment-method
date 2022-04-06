import MACD
import pandas as pd
import re
import datetime
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator

# method 1
# output array of amounts
def hold_save(df, start, end, amount):
    start_price = df['close'][start]
    end_price = df['close'][end]
    btcNumber = amount/start_price
    result = end_price * btcNumber
    return result


#method 2
# equally split for every month
# input: n : number of month
def equally_split(df, start, end, amount, n):
    btcnumber = 0
    each = amount/n
    j = 0
    for i in range(start,end):
        if j%30 == 0:
            btcnumber += each/df['close'][i]
        j = j + 1
    result = btcnumber * df['close'][end]
    return result

# method 3
# signal < MACD - sell
# signal > MACD - buy
def macd_crossover(df,start_idx,end_idx,total_amount):
    amount = total_amount
    btcnumber = 0
    for i in range(start_idx,end_idx):
        if df['macdh_12_26_9'][i] == df['macdh_12_26_9'][i]:
            go = i
            if df['macdh_12_26_9'][i] > 0:
                flag = 1
            if df['macdh_12_26_9'][i] < 0:
                flag = 0
            break
    for i in range(go, end_idx):
        if df['macdh_12_26_9'][i] > 0:
            flag1 = 1
        if df['macdh_12_26_9'][i] < 0:
            flag1 = 0
        if flag1 != flag:
            flag = flag1
            if flag1 > 0:
                btcnumber = amount/df['close'][i]
            if flag1 == 0:
                if btcnumber > 0:
                    amount = btcnumber * df['close'][i]
    return amount

if __name__ == '__main__':
    df = pd.read_csv('BTC.csv')
    #start_d = '2018-03-01'
    #end_d = '2018-10-01'
    start_d = datetime.date(2019, 7, 1)   #起始时间
    end_d = datetime.date(2021, 11, 1)    #结束时间
    start_idx = df.loc[df['Date'] == start_d.__format__('%Y-%m-%d')].index[0]
    end_idx = df.loc[df['Date'] == end_d.__format__('%Y-%m-%d')].index[0]
    total_amount = 100000
    dfPlot = df.loc[start_idx:end_idx, :]
    c = MACD.plotmacd(dfPlot)  # dfPlot 会增加三列，使用macdh_12_26_9这一列

    result1 = []
    for i in range(start_idx,end_idx):
        result1.append(hold_save(df,i,end_idx,total_amount))
    re1_index = result1.index(max(result1))
    re1_bestdate = start_d + datetime.timedelta(days=re1_index)

    result2 = []
    for i in range(start_idx, end_idx):
        startdate = datetime.datetime.strptime(df['Date'][i], '%Y-%m-%d')  #为了算n
        startdate = startdate.date()
        n = ((end_d - startdate).days//30) + 1
        result2.append(equally_split(df,i,end_idx,total_amount,n))
    re2_index = result2.index(max(result2))
    re2_bestdate = start_d + datetime.timedelta(days=re2_index)

    result3 = []
    for i in range(start_idx, end_idx):
        result3.append(macd_crossover(dfPlot,i,end_idx,total_amount))
    re3_index = result3.index(max(result3))
    re3_bestdate = start_d + datetime.timedelta(days=re3_index)



    print(result1[0],result2[0],result3[0])  #按起始时间的三种收益
    print(re1_bestdate,max(result1))  #在限定日期内，method1最佳时间与收益
    print(re2_bestdate,max(result2))  #在限定日期内，method2最佳时间与收益
    print(re3_bestdate, max(result3))
    x1 = df['Date'][start_idx:end_idx]
    y1 = result1
    y2 = result2
    y3 = result3
    x_major_locator = MultipleLocator(((end_d - start_d).days)//5)
    ax = plt.gca()
    # ax为两条坐标轴的实例
    ax.xaxis.set_major_locator(x_major_locator)
    plt.plot(x1,y1,label = 'One time investment')
    plt.plot(x1, y2, label = 'automatic investment')
    plt.plot(x1, y3, label = 'MACD signal method')
    plt.legend()
    plt.show()



    win1, win2, win3 = 0
    for i in range(start_idx, end_idx):
        if result1[i] > result2[i] and result1[i] > result3[i]:
            win1 = win1 + 1
        if result2[i] > result1[i] and result2[i] > result3[i]:
            win2 = win2 + 1
        if result3[i] > result2[i] and result3[i] > result1[i]:
            win3 = win3 + 1
    win1rate = win1 / len(result1)
    win2rate = win2 / len(result1)
    win3rate = win3 / len(result1)




    # plot to compare the three methods


