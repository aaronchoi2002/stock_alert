# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 12:18:48 2023

@author: USER
"""

import yfinance as yf
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder

st.header("Stock alert system_v03")


def show_grid(newline):
    df = pd.read_csv("Barry_stock_list_2023.csv")
    df = df.fillna("0")
    df = df.set_index('Symbol')

    tickers = df.index.to_list()
    price = yf.download(tickers, period="5d", interval="15m")["Adj Close"].T
    price = price.iloc[:,-1] # get the latest price
    df["price"] = round(price,2)
    df.reset_index(inplace=True)
    
    if newline == 'yes':
        ticker = st.sidebar.text_input('Add new ticker')
        alert = st.sidebar.text_input('Add new alert')
        remark = st.sidebar.text_input('Add new remark')
        data = [[ticker, alert, remark,""]]
        df_empty = pd.DataFrame(data, columns=["Symbol", "Alert", "Remark","price"])
        df = pd.concat([df, df_empty], axis=0, ignore_index=True)

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(editable=True)
    grid_table = AgGrid(
        df,
        height=300,
        gridOptions=gb.build(),
        fit_columns_on_grid_load=True,
        allow_unsafe_jscode=True,
        )
    return grid_table

    
def update(grid_table):
    grid_table_df = pd.DataFrame(grid_table['data'])
    grid_table_df.to_csv('Barry_stock_list_2023.csv', index=False)    
     

def alert(grid_table):
    for index,row in grid_table.iterrows():
        if row.Alert > row.price:
            st.code(f"{row.Symbol} target price: {row.Alert} reached ")

# start

tab1, tab2 = st.tabs(["Result", "Data"])
with tab1:
    addline = st.sidebar.radio('Add New Stock', options=['yes', 'no'], index=1, horizontal=True)
    grid_table = show_grid(addline)
    st.button("Update", on_click=update, args=[grid_table])
    grid_table_df = pd.DataFrame(grid_table['data'])   
    st.markdown("---")  
    alert(grid_table_df)
    
with tab2:
    grid_table_df

    df_export = grid_table_df.to_csv()
    st.download_button(
        label="Download data as CSV",
        data=df_export,
        file_name='Alert.csv',
        mime='text/csv',
)
