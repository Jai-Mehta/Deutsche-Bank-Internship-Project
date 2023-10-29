from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from flask import  Flask
from graphs import *


flask_app = Flask(__name__,instance_relative_config=False)
app = Dash(__name__, server=flask_app,external_stylesheets=[dbc.themes.BOOTSTRAP, 'styles.css'])

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(
                            html.Img(
                                src="assets/dblogo.png",
                                height="50vh",
                                style={}
                            )
                        ),
                        dbc.Col(
                            dbc.NavbarBrand(
                                "EthicoBanking",
                                style={
                                    "font-family": "'Roboto', sans-serif",
                                    "font-size": "2.5vw"
                                }
                            )
                        ),
                    ],
                    align="center"
                ),
                href="#",
                style={"textDecoration": "none"},
            ),
        ]
    ),
    color="primary",
    dark=True,
)

radial_options = [
    "Environment",
    "Innovation",
    "Social",
    "Product Responsibility",
    "Community",
    "Governance",
    "Resource Use",
    "Human Rights",
    "Management",
    "Vulnerable Communities Worker Safety",
    "Human Trafficking",
    "Access In Work Poverty",
    "Forced Labor",
    "Migration Child Labor",
    "Education",
    "Freedom of Assembly",
    "Skills",
    "Just Transition",
    "Access to Justice",
    "Drug Pricing",
    "Labor Relations",
    "AI / Automation",
    "Future of Work",
    "Health",
    "Fake News",
    "Mental Health",
    "Food Safety",
    "Food Substance Misuse",
    "Workplace health Nutrition Hunger",
    "Living Wage Digital Inclusion",
    "Financial Inclusion",
    "Working Conditions",
    "Gender Equality",
    "Climate Change",
    "Water",
    "Food Waste",
    "Water Scarcity Air Quality",
    "Drinkable Water",
    "Crop Yields",
    "Net Zero",
    "Carbon Emissions",
    "Animal Welfare",
    "Ecosystem Collapse",
    "Over fishing",
    "Sea Level Rises",
    "Topsoil Loss",
    "Conduct",
    "Board",
    "Data",
    "Tax",
    "Money Laundering",
    "Workplace Conduct",
    "Financial Crime",
    "Inappropriate Behavior",
    "Anti trust Mis selling",
    "Rate Fixing",
    "Data Misuse",
    "Capacity and Competency",
    "Corporate Tax",
    "Data Stewardship",
    "Tax Avoidance",
    "Bonuses Dividends",
    "Share Buybacks",
    "CEO Pay",
]

radial_dropdown_options = []
for value in radial_options:
    radial_dropdown_options.append(
        {'label': value, 'value': value}
    )

app.layout = html.Div([
    navbar,
    dbc.Row([
        dbc.Col([
            html.P(
                "E, S, and G Contributions to Overall ESG Score"
            )],
            style={
                'text-align':'left',
                # 'font-weight': 'bold',
            }
        ),
        dbc.Col([
            html.Img(
                src="assets/piechartkey.png",
                height="60vh",
                style={
                    'margin-left': '31vw'
                }
            )
        ])
    ],
    style={
        'padding': '10vh 8vw 0vh 8vw'
    }),
    dbc.Row([
        #Jack Pie chart
        dbc.Col(
            [
                html.P(
                    "Deutsche Bank",
                    style={
                        'text-align': 'center'
                    }
                ),
                dcc.Graph(
                    figure=display_pie_chart("Deutsche Bank"),
                    style={
                        "width": "12vw",
                        "height": "25vh",
                        "padding-right": "1.5vw"
                    }
                ),
            ],
            style={
                "padding": "3vw"
            },
            className="piecharts"
        ),
        dbc.Col(
            [
                html.P(
                    "Bank of America",
                    style={
                        'text-align': 'center'
                    }
                ),
                dcc.Graph(
                    figure=display_pie_chart("Bank of America"),
                    style={
                        "width": "12vw",
                        "height": "25vh",
                        "padding-right": "1.5vw"
                    }
                ),
            ],
            style={
                "padding": "3vw"
            },
            className="piecharts"
        ),
        dbc.Col(
            [
                html.P(
                    "JPMorgan Chase & Co",
                    style={
                        'text-align': 'center'
                    }
                ),
                dcc.Graph(
                    figure=display_pie_chart("JPMorgan Chase & Co"),
                    style={
                        "width": "12vw",
                        "height": "25vh",
                        "padding-right": "1.5vw"
                    }
                ),
            ],
            style={
                "padding": "3vw"
            },
            className="piecharts"
        ),
        dbc.Col(
            [
                html.P(
                    "PNC Services",
                    style={
                        'text-align': 'center'
                    }
                ),
                dcc.Graph(
                    figure=display_pie_chart("PNC Financial Services"),
                    style={
                        "width": "12vw",
                        "height": "25vh",
                        "padding-right": "1.5vw"
                    }
                ),
            ],
            style={
                "padding": "3vw"
            },
            className="piecharts"
        ),
        dbc.Col(
            [
                html.P(
                    "Fidelity",
                    style={
                        'text-align': 'center'
                    }
                ),
                dcc.Graph(
                    figure=display_pie_chart("Fidelity"),
                    style={
                        "width": "12vw",
                        "height": "25vh",
                        "padding-right": "1.5vw"
                    }
                ),
            ],
            style={
                "padding": "3vw"
            },
            className="piecharts"
        ),
    ], 
    style={
        'padding': '0vh 5vw 3vh 5vw',
        'margin-top': '0vh'
    }),
    dbc.Row([
        #Diya Time Series
        dbc.Col(
            html.Label(
                "Select a keyword from the dropdown options:"
            )
        ),
        dbc.Col(
            dcc.Dropdown(
                id='time-series-dropdown',
                options=[
                    {'label': 'Emission', 'value': 'Emission'},
                    {'label': 'Environment', 'value': 'Environment'},
                    {'label': 'Resource Use', 'value': 'Resource Use'},
                    {'label': 'Climate Change', 'value': 'Climate Change'},
                    {'label': 'Diversity', 'value': 'Diversity'},
                    {'label': 'Innovation', 'value': 'Innovation'},
                    {'label': 'Community', 'value': 'Community'},
                    {'label': 'Social', 'value': 'Social'},
                    {'label': 'Shareholder', 'value': 'Shareholder'},
                    {'label': 'Governance', 'value': 'Governance'},
                    {'label': 'Management', 'value': 'Management'},
                    {'label': 'Workforce', 'value': 'Workforce'},
                ],
                value='Emission',
                className='dropdown',
            )
        ),
    ],
    style={
        'padding': '8vh 8vw 1vh 8vw'
    }),
    dbc.Row([
        dbc.Col(
            dcc.Graph(
                id='time-series',
                style={
                    'padding': '1.5vw'
                },
                className="border",
            )
        ),
    ],
    style={
        'padding': '3vh 5vw 3vh 5vw'
    }),
    dbc.Row([
        #Jai Radial Graph
        dbc.Col(
            html.Label(
                "Select a keyword from the dropdown options:"
            )
        ),
        dbc.Col(
            dcc.Dropdown(
                id='radial-dropdown',
                options=radial_dropdown_options,
                value='Environment',
                className='dropdown'
            )
        ),
    ],
    style={
        'padding': '8vh 8vw 1vh 8vw'
    }),
    dbc.Row([
        dbc.Col(
            dcc.Graph(
                id='radial',
                style={
                    'padding': '1.5vw'
                },
                className="border"
            )
        ),
    ],
    style={
        'padding': '3vh 5vw 3vh 5vw'
    }),
    dbc.Row([
        dbc.Col(
            #Rishav Histogram
            dcc.Graph(
                figure=display_histogram(),
                style={
                    'padding': '2vw'
                },
                className="border",
            ),
            style={
                'padding': '2vw'
            }
        ),
        dbc.Col(
            #Rishav Icicle
            dcc.Graph(
                figure=display_icicle(),
                style={
                    'padding': '2vw'
                },
                className="border",
            ),
            style={
                'padding': '2vw'
            }
        ),
    ],
    style={
        'padding': '3vh 5vw 3vh 5vw'
    }),
    dbc.Row([
        dbc.Col(
            #Vedangi Map
            html.Label(
                "Select a bank from the dropdown options:"
            )
        ),
        dbc.Col(
            dcc.Dropdown(
                id='map-dropdown',
                options=[
                    {'label': 'Deutsche Bank', 'value': 'Deutsche Bank'},
                    {'label': 'Bank of America', 'value': 'Bank of America'},
                    {'label': 'JPMorgan Chase & Co', 'value': 'JPMorgan Chase & Co'},
                    {'label': 'PNC Financial Services', 'value': 'PNC Financial Services'},
                    {'label': 'Fidelity', 'value': 'Fidelity'},
                ],
                value='Deutsche Bank',
                className='dropdown'
            )
        ),
    ],
    style={
        'padding': '8vh 8vw 1vh 8vw'
    }),
    dbc.Row([
        dbc.Col(
            dcc.Graph(
                id='map',
                style={
                    'padding': '1.5vw'
                },
                className="border",
                config={
                    "scrollZoom": False
                },
            )
        ),
    ],
    style={
        'padding': '3vh 5vw 12vh 5vw'
    }),
    dbc.Row([
        dbc.Col(
            html.P(
                "Articles from DB - 1637"
            )
        ),
        dbc.Col(
            html.P(
                "Articles from BOA - 392"
            )
        ),
        dbc.Col(
            html.P(
                "Articles from JPMC - 324"
            )
        ),
        dbc.Col(
            html.P(
                "Articles from PNC - 564"
            )
        ),
        dbc.Col(
            html.P(
                "Articles from Fidelity - 219"
            )
        ),
    ],
    style={
        'padding': '4vh 5vw 2vh 5vw',
        'background-color': '#0b6efd',
        'color': 'white',
    }),
], 
style={
    'max-width': '100%',
    'overflow-y': 'scroll',
    'overflow-x': 'hidden',
})



@app.callback(
    Output('time-series', 'figure'),
    [Input('time-series-dropdown', 'value')]
)
def update_graph(selected_category):
    return return_time_series(selected_category)



@app.callback(
    Output('radial', 'figure'),
    [Input('radial-dropdown', 'value')]
)
def update_graph(selected_category):
    return plot_radial_gauge(selected_category)



@app.callback(
    Output('map', 'figure'),
    [Input('map-dropdown', 'value')]
)
def update_graph(selected_category):
    return return_maps(selected_category)

# from dash import Dash, html
# from dash import dcc
# from graphs import *
# from flask import  Flask

# app = Flask(__name__,instance_relative_config=False)
# dash_app = Dash(__name__,server=app)

# app.layout = html.Div([
#             dcc.Graph(figure=return_time_series('Emission')),
#             dcc.Graph(figure=return_maps('Fidelity')),
#             dcc.Graph(figure=display_pie_chart('Fidelity')),
#             dcc.Graph(figure=plot_radial_gauge('Board')),
#             # dcc.Graph(id='dash_histogram',figure=display_icicle()),
#             # dcc.Graph(id='dash_histogram',figure=display_icicle())
#         ])

if __name__ == "__main__":
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    flask_app.run(host="127.0.0.1", port=8080, debug=True)

