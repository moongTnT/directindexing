import bt
import streamlit as st
import pandas as pd
from utils.fetch_data import *

def get_market_cap_weigh(pdf, prices, ceiling, idx):
    
    pdf_shares = fetch_shares().set_index(keys="tickers", drop=True)
    
    pdf_shares = pdf_shares.loc[pdf.index]
    
    prices.name="close"
    
    pdf_shares = pd.concat([pdf_shares, prices], axis=1)
    
    pdf_shares.index = idx
    
    pdf_shares["유동시가총액"] = pdf_shares["shares"]*pdf_shares["close"]*pdf_shares["rate"]
    
    pdf_shares.sort_values(by="유동시가총액", inplace=True, ascending=False)
    
    pdf_shares["비중"] = 0
    
    total_sum = pdf_shares["유동시가총액"].sum()
    
    for i, row in pdf_shares.iterrows():
        ratio = row["유동시가총액"]/total_sum
        if ratio > 0.1:
            pdf_shares.loc[i, "비중"] = ceiling
            total_sum = (total_sum - row["유동시가총액"])*(1/(1-ceiling))
        else:
            pdf_shares.loc[i, "비중"] = ratio

    return pdf_shares["비중"]

def WeighCap(pdf, data, name, weigh_data):
    
    weigh_list = []

    for i, prices in weigh_data.iterrows():
        price = prices.copy()
        
        price.index = pdf.index

        tmp = get_market_cap_weigh(pdf, price, 0.1, weigh_data.columns)

        tmp.name = prices.name

        weigh_list.append(tmp)

    weigh_cap = pd.concat(weigh_list, axis=1) 
    weigh_cap = weigh_cap.T
    
    strategy = bt.Strategy(name=name,
                           algos=[
                               bt.algos.SelectAll(),
                               bt.algos.WeighTarget(weigh_cap),
                               bt.algos.Rebalance()
                               ]
                            )
    
    return bt.Backtest(strategy, data)

def WeighEaully(data, name):
    
    if st.session_state["rebalance"] == "1개월":
        p = bt.algos.RunMonthly()
        
    elif st.session_state["rebalance"] == "3개월":
        p = bt.algos.RunQuarterly()
        
    elif st.session_state["rebalance"] == "1년":
        p = bt.algos.RunYearly()
    
    strategy = bt.Strategy(name=name,
                           algos=[
                               bt.algos.SelectAll(),
                               bt.algos.WeighEqually(),
                               bt.algos.RunQuarterly(),
                               bt.algos.Rebalance()
                               ]
                            )
    return bt.Backtest(strategy, data)
