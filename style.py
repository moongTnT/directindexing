
init_css="""
<style>
    @import url(//spoqa.github.io/spoqa-han-sans/css/SpoqaHanSansNeo.css);

    [data-testid="collapsedControl"] {
        display: none
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibliity: hidden;}
    * { font-family: 'Spoqa Han Sans Neo', 'sans-serif' !important; }
    
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-uf99v8.e1g8pov65 > div.block-container.css-1y4p8pa.e1g8pov64 {
        padding: 1rem 1rem !important
    }
    
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-uf99v8.e1g8pov65 > div.block-container.css-1y4p8pa.e1g8pov64 > div:nth-child(1) > div > div:nth-child(2) {
        max-height: auto;
    }
</style>
"""

invest_init_css="""
<style>
    @import url(//spoqa.github.io/spoqa-han-sans/css/SpoqaHanSansNeo.css);

    [data-testid="collapsedControl"] {
        display: none
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibliity: hidden;}
    * { font-family: 'Spoqa Han Sans Neo', 'sans-serif' !important; }
    
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-uf99v8.e1g8pov65 > div.block-container.css-1y4p8pa.e1g8pov64 {
        padding: 1rem 1rem !important
    }
    
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-uf99v8.e1g8pov65 > div.block-container.css-1y4p8pa.e1g8pov64 > div:nth-child(1) > div > div:nth-child(2) {
        max-height: 80px;
    }
</style>
"""

cards_css = {
    "display": "flex",
    "overflow-x": "scroll",
    "scroll-snap-type": "x mandatory",
    
    "margin": 0,

    "&::-webkit-scrollbar-thumb": {
        "border-radius": "92px",
        "background": "#F58220"
    },
    "&::-webkit-scrollbar-track": {
        "border-radius": "92px",
        "background": "#ECEFF4"
    },
    "&::-webkit-scrollbar": {
        "height": "5px"
    },
    
}

card_css = {
    "display": "flex",
    "flex-direction": "column",
    "flex": "0 0 100%",
    "scroll-snap-align": "start",
    "max-width": "120px",
    "border-radius": "15px",
    "box-shadow": "none !important",
    "border": "0",
    "margin": "20px 15px 20px 0",
    "cursor": "pointer",
    "background-color": "#ECEFF4",
}