import streamlit as st
from utils.utils import *
from utils.fetch_data import *
from streamlit_elements import elements, mui, html
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

pdf = fetch_pdf(st.session_state.my_theme_ticker)

st.title(st.session_state.my_theme)

with st.form("my_form"):
    tab_list = ["투자 방식", "구성 종목"]
    tab1, tab2 = st.tabs(tab_list)
    
    if st.form_submit_button("ETF 성과 보기", use_container_width=True):
        st.session_state["name"] = st.session_state["name"]
        
        st.session_state["strategy"] = st.session_state["strategy"]
        st.session_state["rebalance"] = st.session_state["rebalance"]
        st.session_state["volumne"] = st.session_state["volumne"]
        
        switch_page("monitor")
        
    # 운용 방식을 선택한다.
    with tab1:
        name = st.text_input(
            "내 ETF의 이름을 입력해주세요",
            "TIGER",
            key="name"
        )
        
        strategies = st.selectbox(
            "종목들의 비중을 선택해보세요",
            ("시가총액가중", "동일가중"),
            key="strategy"
        )
        
        rebalance = st.selectbox(
            "리밸런싱 주기를 선택해보세요",
            ("1개월", "3개월", "1년"),
            index=1,
            key="rebalance"
        )

    # 구성 종목을 선택한다.
    with tab2:        
        pdf = pdf.head(10)
        
        with elements("dataframe"):
            cols = pdf.columns

            table_bodys = []

            index=1
            for ticker, row in pdf.iterrows():
                table_row = [
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
                    mui.TableCell(
                        mui.Typography(row["cmp_name"],
                                       sx={"font-weight": "bold"}, component="span"),
                        mui.Chip(label=row["mkt"],
                                component="span",
                                size="small",
                                sx={"ml": "5px",
                                    "font-size": "x-small",
                                    "font-weight": "bold"}),
                        align="left",
                        sx={"padding": "10px 2px 10px 10px"}
                    ),
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
            
            
        
    
    
