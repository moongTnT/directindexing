import streamlit as st
from utils.utils import *
from utils.fetch_data import *
from streamlit_elements import elements, mui
from streamlit_extras.switch_page_button import switch_page

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

st.markdown(
    f"""
    ## {st.session_state["my_theme_info"]["theme_name"]}
    🤔 {st.session_state["my_theme_info"]["base_index_name"]} ETF에 포함되어 있는 기업들을 모아봤어요.
    
    ✔ 구성종목 편집에서 제외할 종목을 선택해주세요.
    
    ✔ 투자방식 편집에서 각 종목들의 비중과 리밸런싱 주기를 선택해주세요.
    """
)
    
tab_list = ["구성종목 편집", "투자방식 편집"]

tab1, tab2 = st.tabs(tab_list)

with tab1:
    with elements("dataframe"):
        
        def handle_click(index):
            def f(e):
                del st.session_state["invest_theme_pdf"][index-1]
            return f
        
        table_bodys = []
        index=1
        for stock in st.session_state["invest_theme_pdf"]:
            ticker=stock["tickers"]
            cmp_name=stock["cmp_name"]
            market=stock["market"]
            
            table_row = [
                
                # 주황색 숫자 인덱스
                mui.TableCell(
                    mui.Typography(index,
                                   color="#F58220",
                                   sx={"font-weight": "bold"}),
                    align="right",
                    sx={
                        "padding": "10px 10px 10px 0",
                        "width": "0%",
                        }
                    ),
                
                # 기업 로고
                mui.TableCell(
                    mui.Avatar(
                        alt = str(ticker),
                        src=f"{cdn}/{str(ticker)}.png"
                    ),
                    sx={
                        "padding": "10px 2px 10px 0px",
                        "width": "0%"
                        }
                ),
                
                #  기업 이름
                mui.TableCell(
                    mui.Typography(cmp_name,
                                   sx={"font-weight": "bold"}, component="span"),
                    mui.Chip(label=market,
                            component="span",
                            size="small",
                            sx={"ml": "5px",
                                "font-size": "x-small",
                                "font-weight": "bold"}),
                    align="left",
                    sx={"padding": "10px 2px 10px 10px"}
                ),
                
                # 삭제 버튼
                mui.TableCell(
                    mui.IconButton(
                        mui.icon.Delete(),
                        onClick=handle_click(index)
                    ),
                    align="right",
                )
            ]
            
            table_bodys.append(mui.TableRow(*table_row))
            index += 1
        mui.TableContainer(
            mui.Table(
                mui.TableBody(
                    *table_bodys
                ),
                sx={"th, td": {"borderBottom": "none",}}
            )
        )
        
# 운용 방식을 선택한다.
with tab2:
    with st.form("ETF 성과 보기"):
        strategies = st.selectbox(
            "종목들의 비중을 선택해보세요",
            ("시가총액가중", "동일가중"),
            index=0,
        )

        rebalance = st.selectbox(
            "리밸런싱 주기를 선택해보세요",
            ("1개월", "3개월", "1년"),
            index=1,
        )

        name = st.text_input(
            "나만의 ETF의 이름을 입력해주세요",
            "TIGER",
        )

        if st.form_submit_button("ETF 성과 보기", use_container_width=True):
            st.session_state["invest_strategy_info"]["user_etf_name"]=name
            st.session_state["invest_strategy_info"]["comp_method"]=strategies
            st.session_state["invest_strategy_info"]["rebalance"]=rebalance

            st.write(st.session_state)

            switch_page("monitor")
            
