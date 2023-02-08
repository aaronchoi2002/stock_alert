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
    df = pd.read_csv("Barry_stock_list_2023.csv", index_col=False)
    df = df.fillna("0")


    
    if newline == 'yes':
        ticker = st.sidebar.text_input('Add new ticker')
        alert = st.sidebar.number_input('Add new alert')
        remark = st.sidebar.text_input('Add new remark')
        data = [[ticker, alert, remark,""]]
        df_empty = pd.DataFrame(data, columns=["Symbol", "Alert", "Remark","price"])
        df = pd.concat([df, df_empty], axis=0, ignore_index=True)
        
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)
    gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren=True, groupSelectsFiltered=True)
    gb.configure_pagination(enabled=True)
    grid_table = AgGrid(
        df,
        height=300,
        gridOptions=gb.build(),
        reload_data=False,
        fit_columns_on_grid_load=True,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
        )
    return grid_table

    
def update(grid_table):
    # df = df.set_index('Symbol')
    grid_table_df = pd.DataFrame(grid_table['data'])
    grid_table_df = grid_table_df.set_index('Symbol')
    tickers = grid_table_df.index.to_list()
    price = yf.download(tickers, period="5d")["Adj Close"].T
    price = price.iloc[:,-1] # get the latest price
    grid_table_df["price"] = round(price,2)
    grid_table_df.reset_index(inplace=True)
    # grid_table_df = pd.DataFrame(grid_table['data'])
    grid_table_df.to_csv('Barry_stock_list_2023.csv', index=False)    
     

def alert(grid_table):
    for index,row in grid_table.iterrows():
        if row.Alert > row.price:
            st.code(f"{row.Symbol} target price: {row.Alert} reached ")
            
    

# start

tab1, tab2 = st.tabs(["Alert", "Data"])
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
