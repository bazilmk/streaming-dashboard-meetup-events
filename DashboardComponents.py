import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

plot_h, plot_w, plot_m = 432, 920, 0 

title_header = html.Div([        
            html.H1(
                children="Real-time Streaming Dashboard (Meetup RSVPs)",
                style={
                    'fontSize': 32,
                    'textAlign': 'center'
                }
            )
        ])


statistics_header = html.Div([
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        dbc.Card([dbc.CardHeader("Total RSVPs"), 
                                                                  dbc.CardBody(
                                                            [
                                                                html.H5(
                                                                    className="card-title",
                                                                ),
                                                                html.P("-",  id="total_rsvps", className="card-text"),
                                                            ]
                                                        )], color="primary", inverse=True
                                                        )
                                                    ]
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Card([dbc.CardHeader("Total # of Yes"),
                                                                  dbc.CardBody(
                                                            [
                                                                html.H5(
                                                                    className="card-title",
                                                                ),
                                                                html.P("-", id="yes_responses", className="card-text"),
                                                            ]
                                                        )], color="success", inverse=True
                                                        ), 
                                                    ]
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Card([dbc.CardHeader("Total # of No"),
                                                                  dbc.CardBody(
                                                            [
                                                                html.H5(
                                                                    className="card-title",
                                                                ),
                                                                html.P("-", id="no_responses", className="card-text"),
                                                            ]
                                                        )], color="danger", inverse=True
                                                        ), 
                                                    ]
                                                ),
                                            ]
                                        )
                                    ], className =['col-7', 'ml-0' , 'mr-0', 'mt-0' , 'mb-0']
                                ),
                                dbc.Col(
                                    [                        
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [                        
                                                        dbc.Card([dbc.CardHeader("Attendance Rate (%)"),
                                                                  dbc.CardBody(
                                                            [
                                                                html.H5(
                                                                    className="card-title",
                                                                ),
                                                                html.P("-", id="attendance_percentage", className="card-text"),
                                                            ]
                                                        )], color="secondary", inverse=True
                                                        )
                                                    ]
                                                ),                                    
                                                dbc.Col(
                                                    [dbc.Card([dbc.CardHeader("Last update"),
                                                               dbc.CardBody(
                                                            [
                                                                html.H5(                   
                                                                    className="card-title",
                                                                ),
                                                                html.P("-", id="stream_update_time", className="card-text"),
                                                            ]
                                                        ),
                                                        ], color="dark", inverse=True                                     
                                                    )]
                                                )
                                            ]
                                        )
                                    ], className =['col-5', 'ml-0' , 'mr-0', 'mt-0' , 'mb-0']
                                )
                            ], className= ['justify-content-between', 'ml-2' , 'mr-2', 'mt-2' , 'mb-2'],
                        )
                    ]
                )

#  Interval used to auto-update page without refreshing every 5 seconds
interval = dcc.Interval(
            id = "interval",
            interval = 5000,
            n_intervals = 0
        )

world_map = dcc.Graph(
                id='world-map',
                clickData=None,
            )

world_map_style = {
                'width': plot_w,
                'margin-left': 960 - plot_w - int(plot_m//2),
                'margin-right': plot_m,
                'display': 'inline-block',
                # 'border': '2px black solid'
            }

bar_chart = dcc.Graph(
                id='events-barchart'
            )

bar_chart_style = {
                'width': plot_w,
                'display': 'inline-block',
                # 'border': '2px black solid'
                    }