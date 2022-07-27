import pandas as pd
import os



#change your pathway here  Important!!!
os.chdir('D:\WINNER2')

path = os.getcwd()
files = os.listdir(path)

#Type your keywords into Name1,2,3. If the left name is empty, keep it null. Important!!!
NAME1='adelaide'
NAME2='desal'
NAME3=''



train_csv = list(filter(lambda x:( NAME1 in x and NAME2 in x and NAME3 in x),files))

def column0 (i):
    df = pd.read_csv(train_csv[i], header=0)
    result=pd.concat([df.iloc[0]],axis=0)
    
    Result0=result.drop(['Year','Month','Day'])
    date_index = pd.date_range(str(result.loc['Year'])+str(result.loc['Month'])+str(int(result.loc['Day'])), periods=48, freq='0.5H')
    Result0.index=date_index
    
    a=1
    for a in range(1,len(df)):
        result=pd.concat([df.iloc[a]],axis=0)
        Resulti=result.drop(['Year','Month','Day'])
        
        date_index = pd.date_range(str(int(result.loc['Year']))+'/'+str(int(result.loc['Month']))+'/'+str(int(result.loc['Day'])), periods=48, freq='0.5H')
        Resulti.index=date_index

        Result0=pd.concat([Result0,Resulti],axis=0)
    
    Result0.rename("20"+str(11+i),inplace= True)
    return Result0



result=column0(0)

for i in range(1,len(train_csv)):    
    result=pd.concat([result,column0(i)],axis=1)
result7 = result
result7['Min'] = result.iloc[:, 0:len(train_csv)].min(axis=1)
result7['Max'] = result.iloc[:, 0:len(train_csv)].max(axis=1)
result7['Average'] = result.iloc[:, 0:len(train_csv)].mean(axis=1)
result7['POE90']=result.iloc[:, 0:len(train_csv)].quantile(q=0.1, axis=1)
result7['POE50']=result.iloc[:, 0:len(train_csv)].quantile(q=0.5, axis=1)
result7['POE10']=result.iloc[:, 0:len(train_csv)].quantile(q=0.9, axis=1)




arrays = [result7.index.year,result7.index.month,result7.index.day,result7.index.hour,result7.index.minute]
tuples = list(zip(*arrays))
index = pd.MultiIndex.from_tuples(tuples, names=["Year", "Month","Day","Hour","Minute"])
result7.index=index





result7.to_csv(NAME1+'_'+NAME2+'_'+NAME3+'Result.csv')







