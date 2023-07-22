
init_css="""
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
    
</style>
"""

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
        "height": "5px"
    },
    
}

card_css = {
    "display": "flex",
    "flex-direction": "column",
    "flex": "0 0 100%",
    "scroll-snap-align": "start",
    "margin-right": "15px",
    "max-width": "110px",
    "border-radius": "30px",
    "box-shadow": "none !important",
    "border": "0",
    "margin": "20px 15px 20px 0",
    "cursor": "pointer",
    "background-color": "#ECEFF4",
}