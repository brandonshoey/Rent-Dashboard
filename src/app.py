from dash import Dash, dcc, html, Input, Output
from fundamentals import getMarkets, getMarketData
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import dash

# Reading in CoStar Market data
markets = getMarkets()

app = Dash(__name__)
server = app.server

app.layout = html.Div(
    children = [
        html.H1(children="Rent Dashboard"),

        dcc.Dropdown(id="my-dropdown", multi=False,
                    options = [{"label": x, "value": x} for x in markets],
                    value = "All"),

        dcc.Graph(id="bar-chart-output", figure={})
    ]
)

# Generate the chart
@app.callback(
    Output(component_id="bar-chart-output", component_property="figure"),
    [Input(component_id="my-dropdown", component_property="value")],
    prevent_initial_callback=False
)
def update_graph(val_chosen):
    if len(val_chosen) > 0:
        df = getMarketData(val_chosen)
        fig = make_subplots(specs = [[{"secondary_y": True}]])

        fig.add_trace(
            go.Scatter(mode="lines+markers", x=df["Date"], y=df["RentGrowth"], name="Rent Growth"),
            secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(mode="lines+markers", x=df["Date"], y=df["AvailableSF"], name="Available SqFt"),
            secondary_y=True,
        )
        fig.update_layout(
            title_text="<b>Rent and Available SqFt Analysis</b>"
        )
        return fig
    elif len(val_chosen) == 0:
        raise dash.exceptions.PreventUpdate
    
if __name__ == "__main__":
    app.run_server(debug=True)