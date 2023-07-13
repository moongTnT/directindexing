import pandas as pd
from functools import wraps
import bt
import streamlit as st
import pymysql

@st.cache_data()
def fetch_data_from_web(tickers, start):
    data = bt.get(tickers=tickers, start=start)
    
    return data/100

def with_db_connection(f):
    """
    함수 f의 시작 전 후에 DB 커넥션 연결과 종료를 해주는 데코레이터 입니다
    """
    @wraps(f)
    def with_db_connection_(*args, **kwargs):
        conn = pymysql.connect(**st.secrets["db_credentials"],
                               cursorclass=pymysql.cursors.DictCursor)
        try:
            ret = f(*args, connection=conn, **kwargs)
        except:
            conn.rollback()
            print("SQL failed")
            raise
        else:
            conn.commit()
        finally:
            conn.close()
        
        return ret
    
    return with_db_connection_

@with_db_connection
def fetch_data_from_db(*args, **kwargs):
    """
    query를 인자로 받아 실행하고 출력을 DataFrame으로 변경해주는 함수입니다
    """
    conn = kwargs.pop("connection")
    query = kwargs.pop("query")
    
    cursor = conn.cursor()
    
    cursor.execute(query)
    
    return pd.DataFrame(cursor.fetchall())

@st.cache_data
def fetch_shares():
    """
    국내 모든 종목들의 발행주식수와 유동비율을 가져옵니다
    """
    
    sql = """
    select * from shares
    """
    
    return fetch_data_from_db(query=sql)
    

@st.cache_data()
def read_stock_prices_from_db(ticker_list, start):
    
    if len(ticker_list) == 1:
        sql = f"""
            select tickers, date, close from kr_price where tickers = "{ticker_list[0]}" and date>=date("{start}")
        """
    else:
        tickers = ","
        tickers = tickers.join(ticker_list)
        
        sql = f"""
        select tickers, date, close from kr_price where tickers in ({tickers}) and date>=date("{start}")
        """
    
    ret = fetch_data_from_db(query=sql)
    
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
    
    return prices

def fetch_prices(tickers, start):
    data = read_stock_prices_from_db(tickers, start)
    
    data = data.dropna()
    
    return data/100

@st.cache_data()
def fetch_etfs():
    sql="""
    SELECT * from etf order by return_3m desc;
    """
    
    ret = fetch_data_from_db(query=sql)
    
    theme_etfs = ret.set_index(keys="tickers", drop=True)

    return theme_etfs

@st.cache_data()
def fetch_pdf(ticker):
    sql = f"""
        select tickers, cmp_name, mkt from pdf where parent_etf_ticker={ticker}
    """
    
    ret = fetch_data_from_db(query=sql)
    
    my_pdf = ret.set_index(keys="tickers")
    
    return my_pdf

@st.cache_data()
def fetch_sector_pdf(ticker):    
    sql = f"""
        select p.tickers, p.mkt, s.sector from pdf p left join kr_sector s on p.tickers=s.tickers where p.parent_etf_ticker={ticker};
    """
    ret = fetch_data_from_db(query=sql)
    
    sector_pdf = ret.set_index(keys="tickers")
    
    return sector_pdf
