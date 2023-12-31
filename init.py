import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import datetime
from dateutil.relativedelta import relativedelta

from utils.utils import *
from utils.fetch_data import *

from streamlit_elements import elements, mui, html

from style import init_css, card_css, cards_css

st.set_page_config(
    initial_sidebar_state='collapsed')

st.markdown(init_css,
    unsafe_allow_html=True,
)

cdn = st.secrets["cdn_credentials"]["host"]

with elements("title"):
    html.img(src="https://www.miraeasset.co.kr/img/pr/ci_img_01.jpg",width=200)
    
tab_list = ["🇰🇷 국내", "🌎 글로벌"]

tab1, tab2 = st.tabs(tab_list)

start = datetime.datetime.today() - relativedelta(months=3)

with tab1:
    choose_init_state()
    
    with elements("my_card"):
        mui.Typography("🤗 나만의 ETF로 만들 테마를 골라주세요.",
                       sx={
                           "fontSize": 15,
                           "fontWeight": "Bold",
                           "fontFamily": "Spoqa Han Sans Neo"
                       })

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
    
st.markdown("*본 서비스는 2023미래에셋증권 빅데이터 페스티벌 과제 제출용이며 어떠한 상업적 의도 및 행위가 없음을 밝힙니다.")
st.markdown("*사용 데이터는 23년 2분기 데이터로 실시간 데이터가 아님을 밝힙니다.")

if st.session_state["is_choose"]:
    st.session_state["is_choose"]=False
    switch_page("invest")