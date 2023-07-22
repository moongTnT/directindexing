import datetime as dt
import pandas as pd
import streamlit as st
from dateutil.relativedelta import relativedelta
from strategy import *
        
def choose_init_state():
    if "choose_theme_info" in st.session_state:
        return
    
    theme_etfs = fetch_etfs()
    
    if "choose_theme_info" not in st.session_state:
        st.session_state["choose_theme_info"] = []
        
    if "my_theme_info" not in st.session_state:
        st.session_state["my_theme_info"] = dict()
        
    if "is_choose" not in st.session_state:
        st.session_state["is_choose"] = False
    
    st.session_state["choose_theme_info"] = []
    for tickers, row in theme_etfs.iterrows():
        st.session_state["choose_theme_info"].append(
            dict(
                theme_name=row["theme"],
                base_index_name=row["etf_name"],
                tickers=tickers,
                returns=row["return_3m"]
            )
        )
        
    if "invest_theme_pdf" not in st.session_state:
        st.session_state["invest_theme_pdf"]=[]
        
    if "invest_strategy_info" not in st.session_state:
        st.session_state["invest_strategy_info"]=dict(
            user_etf_name="TIGER",
            comp_method="cap_weigh",
            rebalance="quarter"
        )
        
def monitor_init(
    *args, 
    **kwargs,
):
    
    start = kwargs.pop("start", dt.datetime.today()-relativedelta(months=12))
    
    rep_ticker = kwargs.pop("rep_ticker", "KPI200")
    rep_name = kwargs.pop("rep_name", "KOSPI200")
    
    base_name = kwargs.pop("base_index_name", None)
    base_ticker = kwargs.pop("tickers", None)
    
    my_tickers = [v["tickers"] for v in args]
    my_name = kwargs.pop("user_etf_name", "TIGER")
    
    rebalance = kwargs.pop("rebalance", "3개월")
    comp_method = kwargs.pop("comp_method", "시가총액가중")
    
    rep_price=fetch_prices(tickers=[rep_ticker], start=start)
    base_price=fetch_prices(tickers=[base_ticker], start=start)
    my_prices=fetch_prices(tickers=my_tickers, start=start)
    
    port_rep=WeighEaully(rep_price,
                         name=rep_name,
                         rebalance=rebalance)
    
    port_base=WeighEaully(base_price,
                          name=base_name,
                          rebalance=rebalance)
    
    port_my=monitor_choose_strategy(prices=my_prices,
                                    comp_method=comp_method,
                                    rebalance=rebalance,
                                    name=my_name)
    
    return [port_rep, port_base, port_my]

def monitor_choose_strategy(
    prices: pd.DataFrame,
    comp_method: str,
    rebalance: str,
    name: str
):    
    prices["my_date"] = prices.index
    
    if rebalance == "1개월":
        prices["Q"] = pd.PeriodIndex(prices.index, freq="M")
    elif rebalance == "3개월":
        prices["Q"] = pd.PeriodIndex(prices.index, freq="Q")
    elif rebalance == "1년":
        prices["Q"] = pd.PeriodIndex(prices.index, freq="A")    
    
    weigh_data = prices.groupby(["Q"]).first()
    
    weigh_data.set_index(keys="my_date", inplace=True, drop=True)
    
    prices.drop(["Q", "my_date"], axis=1, inplace=True)    
        
    if comp_method == "시가총액가중":
        return WeighCap(prices,
                        name=name,
                        weigh_data=weigh_data)
    
    elif comp_method == "동일가중":
        return WeighEaully(prices,
                           name=name,
                           rebalance=rebalance)
    


