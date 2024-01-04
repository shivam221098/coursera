import dash
import pandas as pd
import numpy as np
import dash
from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output

app = dash.Dash(__name__)


def compute_info(airline_data, entered_year):
    # Select data
    df = airline_data[airline_data['Year'] == int(entered_year)]
    # Compute delay averages
    avg_car = df.groupby(['Month', 'Reporting_Airline'])['CarrierDelay'].mean().reset_index()
    avg_weather = df.groupby(['Month', 'Reporting_Airline'])['WeatherDelay'].mean().reset_index()
    avg_NAS = df.groupby(['Month', 'Reporting_Airline'])['NASDelay'].mean().reset_index()
    avg_sec = df.groupby(['Month', 'Reporting_Airline'])['SecurityDelay'].mean().reset_index()
    avg_late = df.groupby(['Month', 'Reporting_Airline'])['LateAircraftDelay'].mean().reset_index()
    return avg_car, avg_weather, avg_NAS, avg_sec, avg_late


@app.callback([
    Output(component_id="carrier-delay", component_property="figure"),
    Output(component_id="weather-delay", component_property="figure"),
    Output(component_id="nas-delay", component_property="figure"),
    Output(component_id="security-delay", component_property="figure"),
    Output(component_id="avg-delay", component_property="figure")
], Input(
    component_id="year-input",
    component_property="value"
))
def get_graph(entered_year):
    # Compute required information for creating graph from the data
    avg_car, avg_weather, avg_NAS, avg_sec, avg_late = compute_info(airline_data, entered_year)

    # Line plot for carrier delay
    carrier_fig = px.line(avg_car, x='Month', y='CarrierDelay', color='Reporting_Airline',
                          title='Average carrrier delay time (minutes) by airline')
    # Line plot for weather delay
    weather_fig = px.line(avg_weather, x='Month', y='WeatherDelay', color='Reporting_Airline',
                          title='Average weather delay time (minutes) by airline')
    # Line plot for nas delay
    nas_fig = px.line(avg_NAS, x='Month', y='NASDelay', color='Reporting_Airline',
                      title='Average NAS delay time (minutes) by airline')
    # Line plot for security delay
    sec_fig = px.line(avg_sec, x='Month', y='SecurityDelay', color='Reporting_Airline',
                      title='Average security delay time (minutes) by airline')
    # Line plot for late aircraft delay
    late_fig = px.line(avg_late, x='Month', y='LateAircraftDelay', color='Reporting_Airline',
                       title='Average late aircraft delay time (minutes) by airline')

    return carrier_fig, weather_fig, nas_fig, sec_fig, late_fig


airline_data = pd.read_csv(
    "data/airline_data.csv",
    encoding="ISO-8859-1",
    dtype={'Div1Airport': str, 'Div1TailNum': str,
           'Div2Airport': str, 'Div2TailNum': str}
)

app.layout = html.Div([
    html.H1("Flight Delay Time Statistics", style={'textAlign': 'center', 'color': '#503D36',
                                                   'font-size': 30}),
    html.Div([
        "Input Year: ",
        dcc.Input(id="year-input", value='2011', type='number', style={'height': '35px', 'font-size': 30})
    ], style={'font-size': 30}),
    html.Br(),
    html.Br(),
    html.Div(
        [
            html.Div(dcc.Graph(id="carrier-delay")),
            html.Div(dcc.Graph(id="weather-delay"))
        ], style={"display": "flex"}
    ),
    html.Div(
        [
            html.Div(dcc.Graph(id="nas-delay")),
            html.Div(dcc.Graph(id="security-delay"))
        ], style={"display": "flex"}
    ),
    html.Div(dcc.Graph(id="avg-delay"), style={"width": "80%"})
])

if __name__ == '__main__':
    app.run_server()
