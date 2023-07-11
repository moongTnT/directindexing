import pandas as pd
import bt
import streamlit as st
import pymysql

@st.cache_data
def fetch_shares():
    conn = pymysql.connect(**st.secrets["db_credentials"],
                       cursorclass=pymysql.cursors.DictCursor)
    cur = conn.cursor()
    
    sql = """
    select * from shares
    """

    cur.execute(sql)
    
    ret = pd.DataFrame(cur.fetchall())
    
    return ret

@st.cache_data()
def fetch_data_from_web(tickers, start):
    data = bt.get(tickers=tickers, start=start)
    
    return data/100
        
@st.cache_data()
def read_stock_prices_from_db(ticker_list, start):
    conn = pymysql.connect(**st.secrets["db_credentials"],
                       cursorclass=pymysql.cursors.DictCursor)
    cur = conn.cursor()
    
    tickers = ","
    tickers = tickers.join(ticker_list)
    
    sql = f"""
    select tickers, date, close from kr_price where tickers in ({tickers}) and date>=date("{start}")
    """
    
    print(sql)
    
    cur.execute(sql)
    
    ret = pd.DataFrame(cur.fetchall())
    
    grouped_df = ret.groupby(by="tickers")

    df_list = []
    cols = []
    for ticker, df in grouped_df:
        cols.append(ticker)
        df.set_index(keys="date", drop=True, inplace=True)
        df_list.append(df.close)

    prices = pd.concat(df_list, axis=1)
    prices.columns = cols
    
    prices.index = pd.to_datetime(prices.index)
    
    conn.close()
    
    return prices

def fetch_data_from_db(tickers, start):
    data = read_stock_prices_from_db(tickers, start)
    
    data = data.dropna()
    
    return data/100

# 01-init.py
@st.cache_data()
def fetch_etfs():
    conn = pymysql.connect(**st.secrets["db_credentials"],
                       cursorclass=pymysql.cursors.DictCursor)
    cur = conn.cursor()

    cur.execute("""
                SELECT * from etf;
                """)
    theme_etfs = pd.DataFrame(cur.fetchall()).set_index(keys="tickers", drop=True)

    conn.close()
    
    return theme_etfs

# 02-invest.py
@st.cache_data()
def fetch_pdf(ticker):
    conn = pymysql.connect(**st.secrets["db_credentials"],
                       cursorclass=pymysql.cursors.DictCursor)
    
    cur = conn.cursor()
    
    sql = f"""
        select tickers, cmp_name, mkt from pdf where parent_etf_ticker={ticker}
    """
    cur.execute(sql)
    
    my_pdf = pd.DataFrame(cur.fetchall()).set_index(keys="tickers")
    
    conn.close()
    
    return my_pdf

@st.cache_data()
def fetch_sector_pdf(ticker):
    conn = pymysql.connect(**st.secrets["db_credentials"],
                       cursorclass=pymysql.cursors.DictCursor)
    
    cur = conn.cursor()
    
    sql = f"""
        select p.tickers, p.mkt, s.sector from pdf p left join kr_sector s on p.tickers=s.tickers where p.parent_etf_ticker={ticker};
    """
    cur.execute(sql)
    
    sector_pdf = pd.DataFrame(cur.fetchall()).set_index(keys="tickers")
    
    conn.close()
    
    return sector_pdf
