# Import necessary libraries
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Load your dataset
try:
    df = pd.read_csv('sampah.csv', skiprows=1)
except pd.errors.ParserError as err:
    print(f"Error reading CSV file - {err}")

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

navbar = dbc.Navbar(
    [
        dbc.Container(html.A("Final Project - Visdat", className="navbar-brand text-light")),
        dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink("1301190343", active=True, href="#", className="text-light", style={'margin-right': '10px'})),
                dbc.NavItem(dbc.NavLink("1301204527", active=True, href="#", className="text-light", style={'margin-right': '10px'})),
                dbc.NavItem(dbc.NavLink(" ", href="#", className="text-light")),
            ],
            pills=True,
            className="ml-auto",
            style={'margin-right': '10px'},
        ),
    ],
    color="dark",
    dark=True,
    style={'border': 'light'}
)

footer = dbc.Container(
    dbc.Row(
        dbc.Col(
            html.P(
                [
                    html.Span('credit by : ', className='mr-2'),
                    html.Span('Eka Yahya Iskandar Syah & Muhamad Omar Dhani' , className='mr-2'),
                    html.A(html.I(className='fab fa-github-square mr-1'), href='https://github.com/ekayahya'),
                    html.A(html.I(className='fab fa-linkedin mr-1'), href='https://www.linkedin.com/in/username/'),
                    html.A(html.I(className='fab fa-twitter-square mr-1'), href='https://twitter.com/username'),
                ],
                className='lead'
            )
        )
    ),
    style={"position": "absolute", "bottom": "0", "width": "100%"}  # Footer
)

body = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id="select_chart",
                options=[
                    {"label": "Pie Chart", "value": "pie"},
                    {"label": "Histogram", "value": "histogram"},
                    {"label": "Line Plot", "value": "line"},
                ],
                value="line",
                style={'width': "100%"},
                className="text-dark mt-4"
            ),
            dcc.Dropdown(
                id="select_provinsi",
                options=[{"label": x, "value": x} for x in df['Provinsi'].unique()],
                multi=False,
                value='Jakarta',
                style={'width': "100%"},
                className="text-dark mt-4"
            ),
            dcc.Dropdown(
                id='select_tahun',
                options=[{"label": 'All', "value": 'All'}] + [{"label": str(year), "value": str(year)} for year in df['Tahun'].unique()],
                value='All',
                className="text-dark mt-4"
            ),
            html.Div(id='output_container', children=[], className="mt-4"),
        ], width=3),
        dbc.Col([
            html.Div(dcc.Graph(id='output_chart', className="mt-4"))
        ], width=9),
    ])
], className="mt-4")


app.layout = html.Div(
    [
        navbar,
        body,
        html.Div(style={"height": "20px"}),  # Adds some space between body and footer
        footer,
    ],
    style={"position": "relative", "min-height": "100vh"},  # Parent div
)

# Define the callback to update the graphs
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='output_chart', component_property='figure')],
    [Input(component_id='select_provinsi', component_property='value'),
     Input(component_id='select_tahun', component_property='value'),
     Input(component_id='select_chart', component_property='value')]
)
def update_graph(option_slctd, year_slctd, chart_slctd):
    dff = df.copy()
    dff = dff[dff["Provinsi"] == option_slctd]

    if year_slctd != 'All':
        dff = dff[dff["Tahun"] == int(year_slctd)]

    container = "Provinsi: {}, Tahun: {}".format(option_slctd, year_slctd)

    chart = None
    title = ""
    if chart_slctd == "pie":
        chart = px.pie(
            data_frame=dff,
            names='Kabupaten/Kota',
            values='Rumah Tangga(ton)',
            template='plotly_dark'
        )
        title = "Pie Chart: Distribusi Sampah Rumah Tangga"
    elif chart_slctd == "histogram":
        chart = px.histogram(
            data_frame=dff,
            x='Kabupaten/Kota',
            y='Rumah Tangga(ton)',
            histfunc='sum',
            template='plotly_dark'
        )
        title = "Histogram: Total Sampah Rumah Tangga"
        
    elif chart_slctd == "line":
        # Sum the 'Rumah Tangga(ton)' column for each year
        dff_sum = dff.groupby('Tahun')['Rumah Tangga(ton)'].sum().reset_index()

        chart = px.line(
            data_frame=dff_sum,
            x='Tahun',
            y='Rumah Tangga(ton)',
            template='plotly_dark'
        )
        title = "Line Plot: Total Sampah Rumah Tangga"
    else:
        chart = px.scatter()  # Default chart if none of the conditions are met
        title = "Default chart"

    chart.update_layout(title=title)

    return container, chart

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
