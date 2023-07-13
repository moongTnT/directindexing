import streamlit as st
import bt
from card_component import card_component
from streamlit_extras.switch_page_button import switch_page
import datetime
from dateutil.relativedelta import relativedelta

from utils.utils import init_user_state
from utils.fetch_data import *

from streamlit_elements import elements, html, mui

st.set_page_config(
    initial_sidebar_state='collapsed')

st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
    
</style>
""",
    unsafe_allow_html=True,
)

cdn = st.secrets["cdn_credentials"]["host"]

st.markdown("""
            ###  **테마형 지수로 시작해보세요**
            """)

tab_list = ["국내 주식", "해외 주식"]

tab1, tab2 = st.tabs(tab_list)

cards_css = {
    "display": "flex",
    "overflow-x": "scroll",
    "scroll-snap-type": "x mandatory",

    "&::-webkit-scrollbar-thumb": {
        "border-radius": "92px",
        "background": "#F58220"
    },
    "&::-webkit-scrollbar-track": {
        "border-radius": "92px",
        "background": "#ECEFF4"
    },
    "&::-webkit-scrollbar": {
        "height": "12px"
    },
    
}

card_css = {
    "display": "flex",
    "flex-direction": "column",
    "flex": "0 0 100%",
    "scroll-snap-align": "start",
    "margin-right": "15px",
    "border-color": "#ECEFF4",
    "max-width": "110px",
    "border-radius": "20px",
    "margin": "20px 15px 30px 0",
    "cursor": "pointer"
}

start = datetime.datetime.today() - relativedelta(months=3)

theme_etfs = fetch_etfs()

ticker = theme_etfs.index.to_list()[0]

with tab1:
    with elements("my_card"):
        init_user_state()

        def allocate_state(key, val):
            st.session_state[key]=val

        def handle_click(theme, theme_ticker, name):
            def f(e):
                allocate_state("is_clicked", True)
                allocate_state("my_theme_ticker", theme_ticker)
                allocate_state("my_theme", theme)    
                allocate_state("my_base_index_name", name)
            return f

        card_list = []

        for ticker, row in theme_etfs.iterrows():
            ret_str = "+"+str(row["return_3m"]) if row["return_3m"] >= 0 else str(row["return_3m"])
            if row["return_3m"] >= 0:
                ret_comp = mui.Typography(f'{ret_str}%', variant="caption", componet='span', color="red", sx={"font-weight": "bold"})
            else:
                ret_comp = mui.Typography(f'{ret_str}%', variant="caption", componet='span', color="blue", sx={"font-weight": "bold"})
            tmp_card = mui.Card(
                    mui.CardContent(
                            mui.Avatar(
                                src=f"{cdn}/{ticker}.svg",
                                alt=ticker,
                                sx={"width": "30px",
                                    "height": "30px"}
                                ),
                            mui.Typography(row["theme"], sx={"font-weight": "bold", "font-size": "12px"}),
                            mui.Typography("1년 ", variant="caption", component="span"),
                            ret_comp,
                    ),
                onClick=handle_click(theme=row["theme"],
                                     theme_ticker=ticker,
                                     name=row["etf_name"]),
                sx=card_css,
            )
            card_list.append(tmp_card)

        mui.Container(
            *card_list,
            sx=cards_css)
with tab2:
    st.text("🤗 준비 중이에요~ 조금만 기다려 주세요! 🤗")

if st.session_state.is_clicked:
    switch_page("invest")
    