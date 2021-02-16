import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import time
import dash_bootstrap_components as dbc
import DashboardComponents as components

from cassandra.cluster import Cluster


class PlotlyVisualizations:
    ''' Class containing functions to create plots '''

    def world_map(self, df, x_col, y_col, label_col, chart_title):

        map_json = {

            'data': [go.Choropleth(
                locations=df[x_col],
                z=df[y_col],
                text=df[label_col],
                colorscale='blues',
                marker_line_color='darkgray',
                marker_line_width=0.5,
                colorbar_title="Total<br>RSVP's"
            )],

            'layout': go.Layout(
#                title_text='Worldwide RSVP Map',
                width=plot_w,
#                height=plot_h,
                margin={'b': 0, 't': 0, 'r': 0, 'l': 0},
                clickmode='event+select',
                geo=dict(
                    showframe=False,
                    showcoastlines=False,
                    landcolor = 'rgb(230, 230, 230)',
                    showland = True
                )
            )
        }

        return map_json
    
    def bar_chart(self, dff, x_col, y_col, chart_title, barmode, data):

        bar_json = {

            'data': data,

            'layout': go.Layout(
                title=chart_title,
                width=plot_w,
                height=plot_h,
                barmode=barmode,
                xaxis={'title': 'Event Name'},
                yaxis={'title': 'Total # of responses'},
                showlegend=True
            )


        }

        return bar_json
    
    def create_go_bar(self, df, x_col, y_col, name):

        return go.Bar(
            x=df[x_col],
            y=df[y_col],
            text=df['group_name'],
            name=name,
            marker_color='rgb(62,65,60)'
           )


plot_h, plot_w, plot_m = 432, 920, 0

# Create class objects
plotly_obj = PlotlyVisualizations()

cluster = Cluster(['0.0.0.0'],port=9042)
session = cluster.connect('meetups_space', wait_for_all_pools=True)
session.execute('USE meetups_space')


def pandas_factory(col_names, rows):
    return pd.DataFrame(rows, columns=col_names)

session.row_factory = pandas_factory
session.default_fetch_size = None


''' Layout Code'''
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(children=[  
         html.Div([components.title_header]),
         html.Div([components.statistics_header]),
         html.Div([
                 html.Div(components.world_map, style=components.world_map_style),
                 html.Div(components.bar_chart, style=components.bar_chart_style)
                 ], style={'display': 'inline-block'}, className='row'),
         html.Div([components.interval])
         ])


@app.callback(
    [
        dash.dependencies.Output("total_rsvps", "children"),
        dash.dependencies.Output("yes_responses", "children"),
        dash.dependencies.Output("no_responses", "children"),
        dash.dependencies.Output("attendance_percentage", "children"),
        dash.dependencies.Output("stream_update_time", "children")
    ],
        [dash.dependencies.Input('interval', 'n_intervals')]
)
def update_stats_header(data):
        
    query = "SELECT * \
    FROM response_statistics" 
    rslt = session.execute(query, timeout=None)    
    df = rslt._current_rows
    
    yes = df[df['response'] == 'yes']['total_rsvps'].values[0]
    no = df[df['response'] == 'no']['total_rsvps'].values[0]
    total = float(yes + no)
    attendance = str(round((yes / total) * 100, 2)) + '%' 
  
    return total, yes, no, attendance, time.strftime("%Y-%m-%d %H:%M:%S")
    
    
@app.callback(
    dash.dependencies.Output('world-map', 'figure'),
    [
    dash.dependencies.Input('interval', 'n_intervals')
    ]
)
def update_world_map(json):

    query = "SELECT * \
    FROM country_statistics"    
    rslt = session.execute(query, timeout=None)
    df = rslt._current_rows
    return plotly_obj.world_map(
        df, 'event_country', 'total_rsvps', 'event_country', 'event_country')


@app.callback(
     dash.dependencies.Output('events-barchart', 'figure'),
     [ 
      dash.dependencies.Input('interval', 'n_intervals'),
      dash.dependencies.Input('world-map', 'clickData'),
      dash.dependencies.Input('world-map', 'selectedData')
     ]
)
def update_bar_chart(json, clickData, selectedData):
    if selectedData != None:
        selected_country = selectedData['points'][0]['text']
        query = "SELECT * \
        FROM event_statistics"
        rslt = session.execute(query, timeout=None)
        df = rslt._current_rows
        df = df[df['event_country'] == selected_country].sort_values('total_rsvps', ascending=False).head(10)
        
        global_bar_data = [plotly_obj.create_go_bar(
            df, 'event_name', 'total_rsvps', 'Event RSVPs<br>(Group name <br>on Hover)')]
        return plotly_obj.bar_chart(df, 'event_name', 'total_rsvps', selected_country + ' - Top trending events', 'group', global_bar_data)
        
    else:
        query = "SELECT * \
        FROM event_statistics"
        rslt = session.execute(query, timeout=None)
        df = (rslt._current_rows).sort_values('total_rsvps', ascending=False).head(10)
        
        global_bar_data = [plotly_obj.create_go_bar(
            df, 'event_name', 'total_rsvps', 'Event RSVPs<br>(Group name <br>on Hover)')]
        return plotly_obj.bar_chart(df, 'event_name', 'total_rsvps', 'Worldwide - Trending events (Top 10)', 'group', global_bar_data)


if __name__ == '__main__':
    app.run_server(debug=False)
