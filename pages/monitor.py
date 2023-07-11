import streamlit as st
from utils.utils import *
from utils.fetch_data import *
import datetime as dt
import bt
from dateutil.relativedelta import relativedelta
from streamlit_elements import elements, mui, html
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

pdf = fetch_sector_pdf(st.session_state.my_theme_ticker)
ticker_pdf = fetch_pdf(st.session_state.my_theme_ticker)
ticker_list = pdf.index.to_list()
        
start = dt.datetime.today() - relativedelta(months=12)

ports = init(st.session_state.my_theme_ticker,
             start,
             pdf,
             ticker_list)

ret = bt.run(*ports)

prices = ret._get_series(freq=None)

my_ret = round(prices.rebase().iloc[-1, -1], 2)

with elements("Title"):
    mui.Typography(f"{st.session_state['name']} ", sx={"font-weight": "600"}, variant="h6", component="span", color="#F58220")
    if st.session_state["strategy"] == "시가총액가중":
        mui.Typography(f"{st.session_state['my_theme']}", sx={"font-weight": "600"}, variant="h6", component="span")
    else:
        mui.Typography(f"{st.session_state['my_theme']} {st.session_state['strategy']}", sx={"font-weight": "600"}, variant="h6", component="span")
    mui.Typography(f" ETF", sx={"font-weight": "600", }, variant="h6", color="#043B72", component="span")
    mui.Typography(f"{pdf.shape[0]},000 원", variant="h4")
    mui.Typography("1년 수익률 ", variant="body2", sx={"color": "grey"}, component="span")
    if my_ret >= 100:
        mui.Typography(f"+{str(round(my_ret-100, 2))}%", variant="body2", sx={"color": "red"}, component="span")
    else:
        mui.Typography(f"-{str(round(100-my_ret, 2))}%", variant="body2", sx={"color": "blue"}, component="span")
    
tab1, tab2, tab3, tab4, tab5 = st.tabs(["수익", "손실", "리밸런싱 내역", "섹터 구성", "상위 5개 종목"])

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
    
with tab4:
    
    pdf = pd.concat([pdf, st.session_state["pdf_last_ret"]], axis=1)
    pdf.rename(columns={st.session_state['pdf_last_ret'].name: "전일대비"}, inplace=True)
    
    # st.dataframe(pdf, use_container_width=True)
    
    # st.dataframe(pdf["sector"].value_counts())
    
    sector_df = pdf["sector"].value_counts()
    
    fig = px.pie(sector_df,
                 values="count",
                 names=sector_df.index,
                 color_discrete_sequence=px.colors.sequential.Oranges_r,
                 hole=.7)
    st.plotly_chart(fig, use_container_width=True)
    
with tab5:
    cdn = st.secrets["cdn_credentials"]["host"]
    ticker_pdf = ticker_pdf.head()
    with elements("pdf"):
        cols = ticker_pdf.columns
        table_bodys = []
        index=1
        for ticker, row in ticker_pdf.iterrows():
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
    
if st.button(f"TIGER {st.session_state['my_theme']} ETF 사러가기", use_container_width=True): # pdf or csv 다운로드
    st.text("hello")
