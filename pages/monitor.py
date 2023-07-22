import streamlit as st
from utils.utils import *
from utils.fetch_data import *

import bt

from streamlit_elements import elements, mui
import plotly.express as px

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

ports = monitor_init(
    *st.session_state["invest_theme_pdf"],
    **st.session_state["my_theme_info"],
    **st.session_state["invest_strategy_info"]
)

ret = bt.run(*ports)
prices = ret._get_series(freq=None)
my_ret = round(prices.rebase().iloc[-1, -1], 2)

strategy_info = st.session_state["invest_strategy_info"]
theme_info = st.session_state["my_theme_info"]
theme_pdf = st.session_state["invest_theme_pdf"]

with elements("Title"):
    
    mui.Typography(f"{strategy_info['user_etf_name']} ", sx={"font-weight": "600"}, variant="h6", component="span", color="#F58220")
    if strategy_info["comp_method"] == "시가총액가중":
        mui.Typography(f"{theme_info['theme_name']}", sx={"font-weight": "600"}, variant="h6", component="span")
    else:
        mui.Typography(f"{theme_info['theme_name']} {strategy_info['comp_method']}", sx={"font-weight": "600"}, variant="h6", component="span")
        
    mui.Typography(f" ETF", sx={"font-weight": "600", }, variant="h6", color="#043B72", component="span")
    mui.Typography(f"{len(theme_pdf)},000 원", variant="h4")
    
    mui.Typography("1년 전보다 ", variant="body2", sx={"color": "grey"}, component="span")
    if my_ret >= 100:
        mui.Typography(f"+{str(round(my_ret-100, 2))}%", variant="body2", sx={"color": "red"}, component="span")
    else:
        mui.Typography(f"-{str(round(100-my_ret, 2))}%", variant="body2", sx={"color": "blue"}, component="span")
        
tab1, tab2, tab3 = st.tabs(["수익", "손실", "리밸런싱 내역"])
    
with tab1:

    fig = px.line(ret._get_series(freq=None).rebase())
    
    fig.update_layout(
        xaxis_rangeselector_bordercolor="#ffffff",
    )
    fig.update_layout(
        legend_title=None,
        legend=dict(
            x=0.05,
            y=0.95
        )
    )
    
    fig.update_yaxes(title=None, showgrid=False, visible=False)
    fig.update_xaxes(title=None)
    
    fig.data[0].line.color = "#84888B"
    fig.data[1].line.color = "#043B72"
    
    if len(fig.data)>=3:
        fig.data[2].line.color = "#F58220"
    
    st.plotly_chart(fig, use_container_width=True)
    
with tab2:
    # MDD
    fig = px.area(ret._get_series(freq=None).rebase().to_drawdown_series())
    
    fig.data[0].line.color = "#84888B"
    fig.data[1].line.color = "#043B72"
    
    if len(fig.data)>=3:
        fig.data[2].line.color = "#F58220"
    
    fig.update_layout(
        showlegend=False
    )
    
    fig.update_yaxes(title=None, showgrid=False)
    fig.update_xaxes(title=None)
    
    st.plotly_chart(fig, use_container_width=True)
    
with tab3:
    fig = px.area(ret.get_security_weights(-1), color_discrete_sequence=px.colors.sequential.Oranges,)
    
    for d in fig.data:
        d.fillcolor=d.line.color
    
    fig.update_layout(yaxis_range=[0, 1], showlegend=False)
    fig.update_yaxes(title=None, showgrid=False, visible=False)
    fig.update_xaxes(title=None)
    
    st.plotly_chart(fig, use_container_width=True)
        
if st.button(f"{strategy_info['user_etf_name']} {theme_info['theme_name']} ETF 사러가기", use_container_width=True): # pdf or csv 다운로드
    st.text("hello")
    