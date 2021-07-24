import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
from dash.dependencies import Input, Output, State
from datetime import datetime
import pandas as pd
from math import floor
from collections import OrderedDict


# check if traker file exists, if not, create it
try:
    events = pd.read_csv("Baby_Events.csv")
except IOError as e:
    pd.DataFrame(columns=["Event Type", "Start", "Duration", "Source", "Ounces",
                          "Size", "Quality", "Comment"]).to_csv("Baby_Events.csv", index=False)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

submit_button_style = {
    'background-color': '#0064f2',
    'color': 'white',
}

now_botton_style = {
    'background-color': '#00def2',
    'color': 'black',
}


app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ])

app.layout = html.Div([
    dcc.Tabs(id='tabs', value='event-input', children=[
        dcc.Tab(label='Input', value='event-input'),
        dcc.Tab(label='History', value='tables'),
        dcc.Tab(label='Analytics', value='visuals'),
    ]),
    html.Div(id='tab-content')
])


def calc_duration(start, end):
    st = datetime.strptime(start, "%Y-%m-%d %I:%M %p")
    nd = datetime.strptime(end, "%Y-%m-%d %I:%M %p")
    duration = (nd - st)
    return "%dh %dm" % (floor(duration.total_seconds() / 3600), floor((duration.seconds % 3600) / 60))


@app.callback(Output('tab-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'event-input':
        return html.Div([
            html.H5('Event Input', style={"font-size": "20px", "text-decoration": "underline"}),
            # Buttons to select what kind of event
            dcc.RadioItems(
                id='event-type',
                options=[
                    {'label': 'Feeding', 'value': 'Food'},
                    {'label': 'Potty', 'value': 'Potty'},
                    {'label': 'Sleep', 'value': 'Sleep'}
                ],
                value='Food',
                labelStyle={'display': 'inline-block'}
            ),
            # Add a generic Div which will be updates with input fields based on the event type
            html.Div(id='input-fields'),
            # placeholder for testing
            html.P(id='placeholder'),
            html.P(id='placeholder2'),
            html.P(id='placeholder3')
        ])
    elif tab == 'tables':
        ## import csv and prep it for viewingevents.data[::-1]
        events = pd.read_csv("Baby_Events.csv")[::-1].iloc[0:25]
        return html.Div([
            html.H3('Last 50 events'),
            dash_table.DataTable(
                id='table-editing-simple',
                columns=(
                        [{'id': p, 'name': p} for p in events.columns]
                ),
                data=[
                    {param: row[param] for param in events.columns} for ind, row in events.iterrows()
                ],
                editable=True
            ),
            html.P(id='placeholder4')
        ])
    elif tab == 'visuals':
        return html.Div([
            html.H3('This will have some graphs / analysis built from the tables')
        ])


@app.callback(Output('input-fields', 'children'),
              Input('event-type', 'value'))
def display_available_inputs(event_type):
    if event_type == "Food":
        return html.Div([
            html.Div([
                html.Div(
                    html.H6('Start', style={"font-size": "18px"}),
                    style={'display': 'inline-block', 'width': '20%'}
                ),
                html.Div(
                    dcc.Input(
                        id='start-feed-time',
                        type='text',
                        value=datetime.now().strftime("%Y-%-m-%-d %Y-%m-%-d %-I:%M %p"),
                        style={'width': '90%'}
                    ),
                    style={'display': 'inline-block', 'width': '45%'}
                ),
                html.Div(
                    html.Button('Now', id='update-start-feed-time', style=now_botton_style),
                    style={'display': 'inline-block', 'width': '30%'}
                )
            ]),
            html.Div([
                html.Div(
                    html.H6('End', style={"font-size": "18px"}),
                    style={'display': 'inline-block', 'width': '20%'}
                ),
                html.Div(
                    dcc.Input(
                        id='end-feed-time',
                        type='text',
                        value='',
                        style={'width': '90%'}
                    ),
                    style={'display': 'inline-block', 'width': '45%'}
                ),
                html.Div(
                    html.Button('Now', id='update-end-feed-time', style=now_botton_style),
                    style={'display': 'inline-block', 'width': '30%'}
                )
            ]),
            html.Div([
                html.Div(
                    html.H6('Source', style={"font-size": "18px"}),
                    style={'display': 'inline-block', 'width': '20%'}
                ),
                html.Div(
                    dcc.RadioItems(
                        id='food-source',
                        options=[
                            {'label': 'Left', 'value': 'Left'},
                            {'label': 'Right', 'value': 'Right'},
                            {'label': 'Bottle', 'value': 'Bottle'}
                        ],
                        labelStyle={'display': 'inline-block'}
                    ),
                    style={'display': 'inline-block', 'width': '70%'}
                )
            ]),
            html.Div([
                html.Div(
                    html.H6('Ounces', style={"font-size": "18px"}),
                    style={'display': 'inline-block', 'width': '20%'}
                ),
                html.Div(
                    dcc.Input(
                        id='ounces',
                        type='number',
                        value='',
                        style={'width': '90%'}
                    ),
                    style={'display': 'inline-block', 'width': '30%'}
                ),
            ]),
            html.H6('Comment', style={"font-size": "18px"}),
            dcc.Textarea(
                id='feed-comment-text',
                value='',
                style={'width': '98%', 'height': 50},
            ),
            html.Div(
                html.Button('Submit', id='submit-feed-event', style=submit_button_style),
                style={'width': '98%', 'display': 'flex', 'align-items': 'right', 'justify-content': 'right'}
            )
        ])

    elif event_type == "Potty":
        return html.Div([
            html.Div([
                html.Div(
                    html.H6('Time', style={"font-size": "18px"}),
                    style={'display': 'inline-block', 'width': '20%'}
                ),
                html.Div(
                    dcc.Input(
                        id='potty-time',
                        type='text',
                        value=datetime.now().strftime("%Y-%m-%-d %-I:%M %p"),
                        style={'width': '90%'}
                    ),
                    style={'display': 'inline-block', 'width': '45%'}
                ),
                html.Div(
                    html.Button('Now', id='update-potty-time', style=now_botton_style),
                    style={'display': 'inline-block', 'width': '30%'}
                )
            ]),
            html.Div([
                html.Div(
                    html.H6('Size', style={"font-size": "18px"}),
                    style={'display': 'inline-block', 'width': '20%'}
                ),
                html.Div(
                    dcc.RadioItems(
                        id='potty-size',
                        options=[
                            {'label': 'Small', 'value': 'Small'},
                            {'label': 'Normal', 'value': 'Normal'},
                            {'label': 'Beeg, BEEG', 'value': 'Big'}
                        ],
                        value='',
                        labelStyle={'display': 'inline-block'}
                    ),
                    style={'display': 'inline-block', 'width': '80%'}
                )
            ]),
            html.H6('Comment', style={"font-size": "18px"}),
            dcc.Textarea(
                id='potty-comment-text',
                value='',
                style={'width': '98%', 'height': 50},
            ),
            html.Div(
                html.Button('Submit', id='submit-potty-event', style=submit_button_style),
                style={'width': '98%', 'display': 'flex', 'align-items': 'right', 'justify-content': 'right'}
            )
        ])

    elif event_type == "Sleep":
        return html.Div([
            html.Div([
                html.Div(
                    html.H6('Start', style={"font-size": "18px"}),
                    style={'display': 'inline-block', 'width': '20%'}
                ),
                html.Div(
                    dcc.Input(
                        id='start-sleep-time',
                        type='text',
                        value=datetime.now().strftime("%Y-%m-%-d %-I:%M %p"),
                        style={'width': '90%'}
                    ),
                    style={'display': 'inline-block', 'width': '45%'}
                ),
                html.Div(
                    html.Button('Now', id='update-start-sleep-time', style=now_botton_style),
                    style={'display': 'inline-block', 'width': '30%'}
                )
            ]),
            html.Div([
                html.Div(
                    html.H6('End', style={"font-size": "18px"}),
                    style={'display': 'inline-block', 'width': '20%'}
                ),
                html.Div(
                    dcc.Input(
                        id='end-sleep-time',
                        type='text',
                        value='',
                        style={'width': '90%'}
                    ),
                    style={'display': 'inline-block', 'width': '45%'}
                ),
                html.Div(
                    html.Button('Now', id='update-end-sleep-time', style=now_botton_style),
                    style={'display': 'inline-block', 'width': '30%'}
                )
            ]),
            html.Div([
                html.Div(
                    html.H6('Quality', style={"font-size": "18px"}),
                    style={'display': 'inline-block', 'width': '20%'}
                ),
                html.Div(
                    dcc.RadioItems(
                        id='sleep-quality',
                        options=[
                            {'label': 'Meh', 'value': 'Poor'},
                            {'label': 'Normal', 'value': 'Normal'},
                            {'label': 'Great', 'value': 'Great'}
                        ],
                        value='',
                        labelStyle={'display': 'inline-block'}
                    ),
                    style={'display': 'inline-block', 'width': '70%'}
                )
            ]),
            html.H6('Comment', style={"font-size": "18px"}),
            dcc.Textarea(
                id='sleep-comment-text',
                value='',
                style={'width': '98%', 'height': 50},
            ),
            html.Div(
                html.Button('Submit', id='submit-sleep-event', style=submit_button_style),
                style={'width': '98%', 'display': 'flex', 'align-items': 'right', 'justify-content': 'right'}
            )
        ])


@app.callback(Output('start-feed-time', 'value'),
              Input('update-start-feed-time', 'n_clicks'))
def update_start_feed_time(n_clicks):
    new_start_feed_time = datetime.now().strftime("%Y-%m-%-d %-I:%M %p")
    # update some dcc.State to store details about this start time
    return new_start_feed_time


@app.callback(Output('end-feed-time', 'value'),
              Input('update-end-feed-time', 'n_clicks'))
def update_end_feed_time(n_clicks):
    if n_clicks is not None:
        new_end_feed_time = datetime.now().strftime("%Y-%m-%-d %-I:%M %p")
    else:
        new_end_feed_time = ''
    # update some dcc.State to store details about this end time
    return new_end_feed_time


@app.callback(Output('potty-time', 'value'),
              Input('update-potty-time', 'n_clicks'))
def update_start_potty_time(n_clicks):
    new_start_potty_time = datetime.now().strftime("%Y-%m-%-d %-I:%M %p")
    # update some dcc.State to store details about this end time
    return new_start_potty_time


@app.callback(Output('start-sleep-time', 'value'),
              Input('update-start-sleep-time', 'n_clicks'))
def update_start_sleep_time(n_clicks):
    new_start_sleep_time = datetime.now().strftime("%Y-%m-%-d %-I:%M %p")
    # update some dcc.State to store details about this start time
    return new_start_sleep_time


@app.callback(Output('end-sleep-time', 'value'),
              Input('update-end-sleep-time', 'n_clicks'))
def update_end_sleep_time(n_clicks):
    if n_clicks is not None:
        new_end_sleep_time = datetime.now().strftime("%Y-%m-%-d %-I:%M %p")
    else:
        new_end_sleep_time = ''
    # update some dcc.State to store details about this end time
    return new_end_sleep_time


@app.callback(Output('placeholder', 'children'),
              Input('submit-feed-event', 'n_clicks'),
              State('event-type', 'value'),
              State('start-feed-time', 'value'),
              State('end-feed-time', 'value'),
              State('food-source', 'value'),
              State('ounces', 'value'),
              State('feed-comment-text', 'value'))
def submit_feed_event(n_clicks, event_type, start_feed_time, end_feed_time, food_source, ounces, feed_comment_text):
    if n_clicks is not None:
        event_dict = OrderedDict()
        event_dict["Event Type"] = event_type,
        event_dict["Start"] = start_feed_time,
        event_dict["Duration"] = calc_duration(start_feed_time, end_feed_time),
        event_dict["Source"] = food_source,
        event_dict["Ounces"] = ounces,
        event_dict["Size"] = "",
        event_dict["Quality"] = "",
        event_dict["Comment"] = feed_comment_text
        # append event to disk
        event = pd.DataFrame(event_dict, index=[0])
        print(event)
        event.to_csv('Baby_Events.csv', mode='a', header=False, index=False)
    return ''


@app.callback(Output('placeholder2', 'children'),
              Input('submit-potty-event', 'n_clicks'),
              State('event-type', 'value'),
              State('potty-time', 'value'),
              State('potty-size', 'value'),
              State('potty-comment-text', 'value'))
def submit_sleep_event(n_clicks, event_type, potty_time, potty_size, potty_comment_text):
    if n_clicks is not None:
        event_dict = OrderedDict()
        event_dict["Event Type"] = event_type,
        event_dict["Start"] = potty_time,
        event_dict["Duration"] = "",
        event_dict["Source"] = "",
        event_dict["Ounces"] = "",
        event_dict["Size"] = potty_size,
        event_dict["Quality"] = "",
        event_dict["Comment"] = potty_comment_text
        # append event to disk
        event = pd.DataFrame(event_dict, index=[0])
        print(event)
        event.to_csv('Baby_Events.csv', mode='a', header=False, index=False)
    return ''


@app.callback(Output('placeholder3', 'children'),
              Input('submit-sleep-event', 'n_clicks'),
              State('event-type', 'value'),
              State('start-sleep-time', 'value'),
              State('end-sleep-time', 'value'),
              State('sleep-quality', 'value'),
              State('sleep-comment-text', 'value'))
def submit_sleep_event(n_clicks, event_type,  start_sleep_time, end_sleep_time, sleep_quality, sleep_comment_text):
    if n_clicks is not None:
        event_dict = OrderedDict()
        event_dict["Event Type"] = event_type,
        event_dict["Start"] = start_sleep_time,
        event_dict["Duration"] = calc_duration(start_sleep_time, end_sleep_time),
        event_dict["Source"] = "",
        event_dict["Ounces"] = "",
        event_dict["Size"] = "",
        event_dict["Quality"] = sleep_quality,
        event_dict["Comment"] = sleep_comment_text
        # append event to disk
        event = pd.DataFrame(event_dict, index=[0])
        print(event)
        event.to_csv('Baby_Events.csv', mode='a', header=False, index=False)
    return ''


@app.callback(
    Output('placeholder4', 'children'),
    Input('table-editing-simple', 'data'),
    Input('table-editing-simple', 'columns'))
def table_manually_updated(rows, columns):
    # get the events from the table, reverse the order of the rows
    table_events = pd.DataFrame(rows, columns=[c['name'] for c in columns])[::-1]
    # import all events from disk
    all_events = pd.read_csv("Baby_Events.csv")
    update_all_event = pd.concat([all_events.iloc[:(len(all_events) - len(table_events))], table_events], ignore_index=True)
    print(table_events)
    update_all_event.to_csv("Baby_Events.csv", index=False)
    return ''


if __name__ == '__main__':
    app.run_server(debug=False, host="0.0.0.0")
