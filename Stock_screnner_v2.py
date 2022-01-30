#import all the packages we need
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import pickle
import matplotlib.pyplot as plt
import streamlit as st
import plotly
import plotly.express as px
import time
import datetime
from datetime import datetime
#___________________________________________________Function Defines___________________________________________________________________#
#Function Defines
def date2qtr(x):
    QTR=(x.month-1)//3+1
    QTR="Q"+str(QTR)
    return QTR

def date2year(x):
    return x.year

def GM_format(x):
    if(x>=0.4):
        y= 'background-color: green'
    elif(x>=0):
        y='background-color: orange'
    else:
        y='background-color: red'
    return y

def SGA_format(x):#same as liability format
    if( (x<=0.8) and (x>0) ):
        y= 'background-color: green'
    else:
        y=''
    return y

def Interest_format(x):
    if(x>0.15):
        y= 'background-color: red'
    else:
        y=''
    return y

def Debt_format(x):
    if(x>=1):
        y= 'background-color: red'
    else:
        y=''
    return y

def Income_format(x):
    if(x>=0.15):
        y= 'background-color: green'
    else:
        y=''
    return y

def PE_format(x):
    if( (x<=40) and (x>0) ):
        y= 'background-color: green'
    else:
        y=''
    return y

def Ret_Earnings_format(x):
    if(x>=0.0125):
        y= 'background-color: green'
    else:
        y=''
    return y
def Stock_inc_format(x):
    if(x>=0.03):
        y= 'background-color: green'
    else:
        y=''
    return y
#force the layout to be wide
st.set_page_config(layout="wide")
#______________________________________________S&P500________________________________________________________________________________#
#Grab SP500 data
SP500=yf.Ticker('SPY').history(period='max', interval = "3mo")
SP500=SP500.dropna()
#SP500=pd.read_csv(r"C:\Users\cwesterb\Stocks\SP500.csv")
#SP500["Date"]=pd.to_datetime(SP500["Date"])
#SP500 = SP500.set_index('Date')
#print(SP500)
year=[]
qrt=[]
increase=[]
prev_value=SP500['Close'][0]
for row in SP500.itertuples():
    year.append(row.Index.year)
    qrt.append(date2qtr(row.Index))
    increase.append((row.Close-prev_value)/prev_value)
    prev_value=row.Close

SP500['Year']=year
SP500['QTR']=qrt
SP500['SP500 Increase']=increase
SP500_classifier = pickle.load(open('ML_fundamental_analysis_model.sav', 'rb'))

#__________________________________Load the Data set, filter on ticker________________________________________________________________#
companyDF=pd.read_csv(r'C:\Users\cwesterb\Stock Data 11-22-2021\complete_data.csv')


#st.title('Stock Sreener Dashboard')
cols = st.columns(2)
#slect box for picking the company
sim_date = cols[0].date_input('"Current Date" For Simulation')
#remove data after the simulation date
companyDF["Date"] = pd.to_datetime(companyDF["Report Date"], format="%m/%d/%Y")
companyDF=companyDF[companyDF["Date"] <= pd.to_datetime(sim_date, format="%Y/%m/%d")]
#companyDF=pd.read_csv(r'complete_financial_information_2011.csv')
company_list=companyDF.drop_duplicates(subset='Ticker')
company_list=company_list['Ticker'].values
company_ticker = cols[0].selectbox('Ticker:',company_list)

companyDF = companyDF[companyDF['Ticker'] == company_ticker]
filtered_data=companyDF

#need to sort the data
#need to save a copy becasue the sort screws up the plots
plot_data=filtered_data
filtered_data=filtered_data.sort_values(by=['QTR'], ascending=False, kind='mergesort')
filtered_data=filtered_data.sort_values(by=['Year'], ascending=False, kind='mergesort')

#__________________________________Grab the data for plotting________________________________________________________________#

new_temp=filtered_data[["Report Date", "Profit Margin" , "Income pct of Revenue", "SGA pct of Profit", "Interest pct of Income", "Debt pct of Cash",
                            "PE",  "PB",  "Faustmann Ratio", "ROIC", 
                        "ROA", "ROE", "Stock pct Increase"]].copy()
new_style=(new_temp.style
               .applymap(GM_format, subset=['Profit Margin'])
               .applymap(SGA_format, subset=['SGA pct of Profit'])
               .applymap(Interest_format, subset=['Interest pct of Income'])
               .applymap(Income_format, subset=['Income pct of Revenue'])
               .applymap(PE_format, subset=['PE'])
               #.applymap(Ret_Earnings_format, subset=['Retained Earnings Increase'])
               .applymap(Stock_inc_format, subset=["Stock pct Increase"])
               .applymap(Debt_format, subset=['Debt pct of Cash'])
          )#.format("{:.2%}")) 

new_style=new_style.format({'Stock Price':'{:.2f}'})
new_style=new_style.format({"Stock pct Increase":'{:.2%}'})
new_style=new_style.format({'Invested Capital':'{:,.0f}'})
new_style=new_style.format({'Owner Earnings':'{:,.0f}'})
new_style=new_style.format({'Free Cash Flow':'{:,.0f}'})
new_style=new_style.format({'Net Worth':'{:,.0f}'})
new_style=new_style.format({'Market Cap':'{:,.0f}'})
new_style=new_style.format({'PE':'{:.2f}'})
new_style=new_style.format({'PB':'{:.2f}'})
new_style=new_style.format({'PB (Tangible)':'{:.2f}'})
new_style=new_style.format({'Faustmann Ratio':'{:.2f}'})
new_style=new_style.format({'ROIC':'{:.2%}'})
new_style=new_style.format({'Profit Margin':'{:.2%}'})
new_style=new_style.format({'SGA pct of Profit':'{:.2%}'})
new_style=new_style.format({'Income pct of Revenue':'{:.2%}'})
new_style=new_style.format({'Interest pct of Income':'{:.2%}'})
new_style=new_style.format({'Earnings per Share':'{:.2f}'})
new_style=new_style.format({'Debt pct of Cash':'{:.2%}'})
new_style=new_style.format({'ROA':'{:.2%}'})
new_style=new_style.format({'ROE':'{:.2%}'})

#{'B': "{:0<4.0f}", 'D': '{:+.2f}'})
st.dataframe(new_style, height=500)
headings=filtered_data.columns
#cols[1].text(len(headings))

item1 = cols[0].selectbox('Plot1:',headings, index=106)
item2 = cols[0].selectbox('Plot2:',headings)
item3 = cols[0].selectbox('Plot3:',headings)
#__________________________________Run the ML model________________________________________________________________#
#tempX=tempDF.iloc[:, 0:14].values
#temp_predict=SP500_classifier.predict_proba(tempX)
#emp_predict=temp_predict[:,1]
#__________________________________Create the plot of Stock and vs SP500___________________________________________________#
#Add a way to change the start date of the simulation against the SP500

plot2DF=pd.DataFrame(filtered_data[item1])
plot2DF['Date']=filtered_data['Report Date'].values
plot2DF['Date']=pd.to_datetime(plot2DF['Date'])
if(item3 !='Ticker'):
    plot_series=[item1, item2, item3]
    plot2DF[item2]=filtered_data[item2]
    plot2DF[item3]=filtered_data[item3]
elif(item2 !='Ticker'):
    plot_series=[item1, item2]
    plot2DF[item2]=filtered_data[item2]
else:
    plot_series=[item1]
fig2 = px.line(plot2DF,x="Date", y=plot_series)
cols[1].plotly_chart(fig2, use_container_width=True)
