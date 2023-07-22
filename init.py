import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import datetime
from dateutil.relativedelta import relativedelta

from utils.utils import *
from utils.fetch_data import *

from streamlit_elements import elements, mui

from style import init_css, card_css, cards_css

st.set_page_config(
    initial_sidebar_state='collapsed')

st.markdown(init_css,
    unsafe_allow_html=True,
)

cdn = st.secrets["cdn_credentials"]["host"]

st.markdown("""
            ###  **테마형 ETF로 시작해보세요**
            🤗 나만의 ETF로 만들 테마를 골라주세요.
            """)

tab_list = ["🇰🇷 국내 테마", "🌎 글로벌 테마"]

tab1, tab2 = st.tabs(tab_list)

start = datetime.datetime.today() - relativedelta(months=3)

with tab1:
    choose_init_state()
    
    with elements("my_card"):
        

        def allocate_state(key, val):
            st.session_state[key]=val

        def handle_click(theme_info: dict):
            def f(e):
                st.session_state["is_choose"] = True
            
                st.session_state["my_theme_info"]=theme_info
                
                pdf = fetch_pdf(st.session_state["my_theme_info"]["tickers"])
                
                st.session_state["invest_theme_pdf"]=[]
                
                for ticker, row in pdf.iterrows():
                    st.session_state["invest_theme_pdf"].append(
                        dict(
                            tickers=ticker,
                            cmp_name=row["cmp_name"],
                            market=row["mkt"],
                        )
                    )
            return f

        card_list = []

        for theme in st.session_state["choose_theme_info"]:
            ticker=theme["tickers"]
            
            if theme["returns"]>=0:
                ret_str = "+"+str(theme["returns"])
                ret_comp = mui.Typography(f'{ret_str}%', variant="caption", componet='span', color="red", sx={"font-weight": "bold"})
            else:
                ret_str = str(theme["returns"])
                ret_comp = mui.Typography(f'{ret_str}%', variant="caption", componet='span', color="blue", sx={"font-weight": "bold"})
            
            tmp_card = mui.Card(
                    mui.CardContent(
                            mui.Avatar(
                                src=f"{cdn}/{ticker}.svg",
                                alt=ticker,
                                sx={"width": "30px",
                                    "height": "30px"}
                                ),
                            mui.Typography(theme["theme_name"], sx={"font-weight": "bold", "font-size": "12px"}),
                            mui.Typography("1년 ", variant="caption", component="span"),
                            ret_comp,
                    ),
                onClick=handle_click(theme_info=theme),
                sx=card_css,
            )
            card_list.append(tmp_card)

        mui.Container(
            *card_list,
            sx=cards_css)
with tab2:
    st.text("🤗 준비 중이에요~ 조금만 기다려 주세요! 🤗")

if st.session_state["is_choose"]:
    st.session_state["is_choose"]=False
    switch_page("invest")