import bt
import pandas as pd
import streamlit as st
from utils.fetch_data import fetch_data_from_db, fetch_data_from_web


def init_user_state():
    if 'my_theme' not in st.session_state:
        st.session_state['my_theme'] = None

    if 'my_base_index_name' not in st.session_state:
        st.session_state['my_base_index_name'] = None
        
    if 'my_theme_' not in st.session_state:
        st.session_state['my_theme_ticker'] = None
        
    if "name" not in st.session_state:
        st.session_state["name"]=None
        
    if "strategy" not in st.session_state:
        st.session_state["strategy"]="시가총액 비중"
        
    if "rebalance" not in st.session_state:
        st.session_state["rebalance"]="3개월"
        
    if "pdf_last_ret" not in st.session_state:
        st.session_state["pdf_last_ret"]=None
    
    if "volumne" not in st.session_state:
        st.session_state["volumne"]=None

def get_ticker_list(pdf):
    ticker_list = []
    for i, row in pdf.iterrows():
        if row["시장구분"]=="KOSPI":
            ticker_list.append(i+".ks")
        else:
            ticker_list.append(i+".kq")
    return ticker_list

from strategy import *

def choose_strategy(pdf, tickers, start):    
    data = fetch_data_from_db(tickers=tickers, start=start)
    
    data["my_date"] = data.index
    
    if st.session_state["rebalance"] == "1개월":
        data["Q"] = pd.PeriodIndex(data.index, freq="M")
    elif st.session_state["rebalance"] == "3개월":
        data["Q"] = pd.PeriodIndex(data.index, freq="Q")
    elif st.session_state["rebalance"] == "1년":
        data["Q"] = pd.PeriodIndex(data.index, freq="A")    
    
    weigh_data = data.groupby(["Q"]).first()
    
    weigh_data.set_index(keys="my_date", inplace=True, drop=True)
    
    data.drop(["Q", "my_date"], axis=1, inplace=True)    
    
    st.session_state["pdf_last_ret"] = pd.Series(round(data.pct_change().iloc[-1]*100, 2))
    
    if st.session_state["strategy"] == "시가총액가중":
        return WeighCap(pdf, data, "시가총액가중", weigh_data)
    
    elif st.session_state["strategy"] == "동일가중":
        return WeighEaully(data, "동일가중")

def init(bas_ticker, start, pdf, tickers):
    # 대표지수(코스피200)
    rep_data = fetch_data_from_web(tickers=["^KS200"], start=start)
    port_rep = WeighEaully(rep_data, name="코스피200")

    # 기준지수
    bas_data = fetch_data_from_web(tickers=[str(bas_ticker)+'.ks'], start=start)
    port_base = WeighEaully(bas_data, name=st.session_state.my_base_index_name)    
    
    # 나의 지수
    port_my = choose_strategy(pdf, tickers, start)

    ports = [port_rep, port_base, port_my]
    
    return ports