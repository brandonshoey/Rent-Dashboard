from dash import Dash, dash_table, dcc, html, Input, Output, State
import plotly.express as px
from fundamentals import getMarkets, getMarketData
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import dash

# Reading in CoStar market level data
markets = getMarkets()

app = Dash(__name__)
server = app.server

app.layout = html.Div(
    children = [
        html.H1(children="Rent Forecasting Dashboard"),

        dcc.Dropdown(id="my-dropdown", multi=False,
                     options = [{"label": x, "value": x} for x in markets],
                     value = "All"),

        dcc.Graph(id="bar-chart-output", figure={}),
    ]
)

# Callback and function that generates a chart
@app.callback(
    Output(component_id="bar-chart-output", component_property="figure"),
    [Input(component_id="my-dropdown", component_property="value")],
    prevent_initial_callback=False
)
def update_my_graph(val_chosen):
    if len(val_chosen) > 0:
        print(f"Building chart for {val_chosen}")
        df = getMarketData(val_chosen)
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(
            go.Scatter(mode="lines+markers", x=df["Date"], y=df["RentGrowth"], name="Rent Growth"),
            secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(mode="lines+markers", x=df["Date"], y=df["AvailableSF"], name="Available SqFt"),
            secondary_y=True
        )
        fig.update_layout(
            title_text="<b>Rent Forecast Dynamics</b>"
        )
        return fig
    elif len(val_chosen) == 0:
        raise dash.exceptions.PreventUpdate

if __name__ == "__main__":
    app.run_server(debug=True)