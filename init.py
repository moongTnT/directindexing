import streamlit as st
import bt
from card_component import card_component
from streamlit_extras.switch_page_button import switch_page

from utils.utils import init_user_state
from utils.fetch_data import *

st.set_page_config(
    initial_sidebar_state='collapsed')

st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
    tabs-bui3113-tabpanel-0 > div:nth-child(1) {
        overflow-x: scroll;
    }
</style>
""",
    unsafe_allow_html=True,
)

cdn = st.secrets["cdn_credentials"]["host"]

theme_etfs = fetch_etfs()

init_user_state()

st.markdown("""
            ###  **테마형 지수로 시작해보세요**
            """)

tab_list = ["국내 주식", "해외 주식"]

import datetime
from dateutil.relativedelta import relativedelta

start = datetime.datetime.today() - relativedelta(months=3)

ticker = theme_etfs.index.to_list()[0]

tab1, tab2 = st.tabs(tab_list)

with tab1:

    col_list = st.columns(4)
    i=0

    
    for ticker, row in theme_etfs.iterrows():
        # etf_price = bt.get([str(ticker)], start=start)
        with col_list[i%4]:
            if card_component(
                    title=row["theme"],
                    img_path=f"{cdn}/{str(ticker)}.svg",
                    pdf_cnts=ticker,
                    body=row["return_3m"]
                ):
                st.session_state['my_theme']=row['theme']
                st.session_state['my_theme_ticker']=ticker
                st.session_state["my_base_index_name"]=row['etf_name']
                switch_page("invest")      
        i+=1

with tab2:
    st.text("🤗 준비 중이에요~ 조금만 기다려 주세요! 🤗")
