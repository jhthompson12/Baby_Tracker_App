import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import datetime
import pandas as pd
from math import floor
from collections import OrderedDict

# check if tracker file exists, if not, create it
try:
    events = pd.read_csv("Baby_Events.csv")
except IOError as e:
    pd.DataFrame(columns=["Event Type", "Start", "Duration", "Source", "Ounces", "Comment"]).to_csv("Baby_Events.csv",
                                                                                                    index=False)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

submit_button_style = {
    'background-color': '#0064f2',
    'color': 'white',
}

now_botton_style = {
    'background-color': '#00def2',
    'color': 'black',
}

# the number of rows (events) to display on the table
events_to_display = 200

store_id_prefix = ('start-feed-time', 'end-feed-time', 'food-source', 'ounces', 'feed-comment-text', 'potty-time',
                   'potty-type', 'potty-comment-text', 'start-sleep-time', 'end-sleep-time', 'sleep-comment-text')

update_buttons = ('submit-feed-event', 'submit-feed-event', 'submit-feed-event', 'submit-feed-event', 'submit-feed-event',
                  'submit-potty-event' 'submit-potty-event', 'submit-sleep-event' 'submit-sleep-event' 'submit-sleep-event')

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
    html.Div(id='tab-content'),
    # create store objects to store event inputs
    html.Div([dcc.Store(id='%s-store' % name, data={"value": ""}) for name in store_id_prefix]), #, storage_type='session',
    dcc.Location(id="hidden-page-refresh1", refresh=True),
    dcc.Location(id="hidden-page-refresh2", refresh=True),
    dcc.Location(id="hidden-page-refresh3", refresh=True)
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
            html.P(id='placeholder3'),
        ])
    elif tab == 'tables':
        ## import csv and prep it for viewingevents.data[::-1]
        events = pd.read_csv("Baby_Events.csv")[::-1].iloc[0:events_to_display]
        return html.Div([
            html.H3('Last %d events' % events_to_display),
            dash_table.DataTable(
                id='table-editing-simple',
                columns=(
                    [{'id': p, 'name': p} for p in events.columns]
                ),
                data=[
                    {param: row[param] for param in events.columns} for ind, row in events.iterrows()
                ],
                editable=True,
                row_deletable=True
            ),
            html.P(id='placeholder4')
        ])
    elif tab == 'visuals':
        return html.Div([
            html.H3('This will have some graphs / analysis built from the tables')
        ])


@app.callback(Output('input-fields', 'children'),
              Input('event-type', 'value'),
              State("start-feed-time-store", "data"),
              State("end-feed-time-store", "data"),
              State("food-source-store", "data"),
              State("ounces-store", "data"),
              State("feed-comment-text-store", "data"),
              State("potty-time-store", "data"),
              State("potty-type-store", "data"),
              State("potty-comment-text-store", "data"),
              State("start-sleep-time-store", "data"),
              State("end-sleep-time-store", "data"),
              State("sleep-comment-text-store", "data"))
def display_available_inputs(event_type, start_feed_time_data, end_feed_time_data, food_source_data, ounces_data, feed_comment_text_data, potty_time_data, potty_type_data, potty_comment_text_data, start_sleep_time_data, end_sleep_time_data, sleep_comment_text_data):
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
                        value=datetime.now().strftime("%Y-%-m-%-d %Y-%m-%-d %-I:%M %p") if start_feed_time_data["value"] == "" else start_feed_time_data["value"],
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
                        value=end_feed_time_data["value"],
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
                        value=None if food_source_data["value"] == "" else food_source_data["value"],
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
                        value=None if ounces_data["value"] == "" else ounces_data["value"],
                        style={'width': '90%'}
                    ),
                    style={'display': 'inline-block', 'width': '30%'}
                ),
            ]),
            html.H6('Comment', style={"font-size": "18px"}),
            dcc.Textarea(
                id='feed-comment-text',
                value="" if feed_comment_text_data["value"] == "" else feed_comment_text_data["value"],
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
                        value=datetime.now().strftime("%Y-%m-%-d %-I:%M %p") if potty_time_data["value"] == "" else potty_time_data["value"],
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
                    html.H6('Type', style={"font-size": "18px"}),
                    style={'display': 'inline-block', 'width': '20%'}
                ),
                html.Div(
                    dcc.RadioItems(
                        id='potty-type',
                        options=[
                            {'label': 'Poo', 'value': 'Poo'},
                            {'label': 'Pee', 'value': 'Pee'}
                        ],
                        value="" if potty_type_data["value"] == "" else potty_type_data["value"],
                        labelStyle={'display': 'inline-block'}
                    ),
                    style={'display': 'inline-block', 'width': '80%'}
                )
            ]),
            html.H6('Comment', style={"font-size": "18px"}),
            dcc.Textarea(
                id='potty-comment-text',
                value="" if potty_comment_text_data["value"] == "" else potty_comment_text_data["value"],
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
                        value=datetime.now().strftime("%Y-%m-%-d %-I:%M %p") if start_sleep_time_data["value"] == "" else start_sleep_time_data["value"],
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
                        value='' if end_sleep_time_data["value"] == "" else end_sleep_time_data["value"],
                        style={'width': '90%'}
                    ),
                    style={'display': 'inline-block', 'width': '45%'}
                ),
                html.Div(
                    html.Button('Now', id='update-end-sleep-time', style=now_botton_style),
                    style={'display': 'inline-block', 'width': '30%'}
                )
            ]),
            html.H6('Comment', style={"font-size": "18px"}),
            dcc.Textarea(
                id='sleep-comment-text',
                value='' if sleep_comment_text_data["value"] == "" else sleep_comment_text_data["value"],
                style={'width': '98%', 'height': 50},
            ),
            html.Div(
                html.Button('Submit', id='submit-sleep-event', style=submit_button_style),
                style={'width': '98%', 'display': 'flex', 'align-items': 'right', 'justify-content': 'right'}
            )
        ])


@app.callback(Output('start-feed-time', 'value'),
              Input('update-start-feed-time', 'n_clicks'),
              State('start-feed-time-store', 'data'))
def update_start_feed_time(n_clicks, start_feed_time_store):
    if (n_clicks is None) & (start_feed_time_store["value"] != ""):
        new_start_feed_time = start_feed_time_store["value"]
    else:
        new_start_feed_time = datetime.now().strftime("%Y-%m-%-d %-I:%M %p")

    return new_start_feed_time


@app.callback(Output('end-feed-time', 'value'),
              Input('update-end-feed-time', 'n_clicks'),
              State('end-feed-time-store', 'data'))
def update_end_feed_time(n_clicks, end_feed_time_store):
    if n_clicks is None:
        new_end_feed_time = end_feed_time_store["value"]
    else:
        new_end_feed_time = datetime.now().strftime("%Y-%m-%-d %-I:%M %p")
    return new_end_feed_time


@app.callback(Output('potty-time', 'value'),
              Input('update-potty-time', 'n_clicks'),
              State('potty-time-store', 'data'))
def update_start_potty_time(n_clicks, potty_time_store):
    if (n_clicks is None) & (potty_time_store["value"] != ""):
        new_start_potty_time = potty_time_store["value"]
    else:
        new_start_potty_time = datetime.now().strftime("%Y-%m-%-d %-I:%M %p")
    return new_start_potty_time


@app.callback(Output('start-sleep-time', 'value'),
              Input('update-start-sleep-time', 'n_clicks'),
              State('start-sleep-time-store', 'data'))
def update_start_sleep_time(n_clicks, start_sleep_time_store):
    if (n_clicks is None) & (start_sleep_time_store["value"] != ""):
        new_start_sleep_time = start_sleep_time_store["value"]
    else:
        new_start_sleep_time = datetime.now().strftime("%Y-%m-%-d %-I:%M %p")
    return new_start_sleep_time


@app.callback(Output('end-sleep-time', 'value'),
              Input('update-end-sleep-time', 'n_clicks'),
              State('end-sleep-time-store', 'data'))
def update_end_sleep_time(n_clicks, end_sleep_time_store):
    if n_clicks is None:
        new_end_sleep_time = end_sleep_time_store["value"]
    else:
        new_end_sleep_time = datetime.now().strftime("%Y-%m-%-d %-I:%M %p")
    return new_end_sleep_time


@app.callback(Output('hidden-page-refresh1', 'href'),
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
        event_dict["Comment"] = feed_comment_text
        # append event to disk
        event = pd.DataFrame(event_dict, index=[0])
        event.to_csv('Baby_Events.csv', mode='a', header=False, index=False)
        return "/"
    else:
        raise PreventUpdate


@app.callback(Output('hidden-page-refresh2', 'href'),
              Input('submit-potty-event', 'n_clicks'),
              State('potty-time', 'value'),
              State('potty-type', 'value'),
              State('potty-comment-text', 'value'))
def submit_potty_event(n_clicks, potty_time, potty_type, potty_comment_text):
    if n_clicks is not None:
        event_dict = OrderedDict()
        event_dict["Event Type"] = potty_type,
        event_dict["Start"] = potty_time,
        event_dict["Duration"] = "",
        event_dict["Source"] = "",
        event_dict["Ounces"] = "",
        event_dict["Comment"] = potty_comment_text
        # append event to disk
        event = pd.DataFrame(event_dict, index=[0])
        event.to_csv('Baby_Events.csv', mode='a', header=False, index=False)
        return '/'
    else:
        raise PreventUpdate


@app.callback(Output('hidden-page-refresh3', 'href'),
              Input('submit-sleep-event', 'n_clicks'),
              State('event-type', 'value'),
              State('start-sleep-time', 'value'),
              State('end-sleep-time', 'value'),
              State('sleep-comment-text', 'value'))
def submit_sleep_event(n_clicks, event_type, start_sleep_time, end_sleep_time, sleep_comment_text):
    if n_clicks is not None:
        event_dict = OrderedDict()
        event_dict["Event Type"] = event_type,
        event_dict["Start"] = start_sleep_time,
        event_dict["Duration"] = calc_duration(start_sleep_time, end_sleep_time),
        event_dict["Source"] = "",
        event_dict["Ounces"] = "",
        event_dict["Comment"] = sleep_comment_text
        # append event to disk
        event = pd.DataFrame(event_dict, index=[0])
        event.to_csv('Baby_Events.csv', mode='a', header=False, index=False)
        return '/'
    else:
        raise PreventUpdate


for store_name in store_id_prefix:
    store = store_name + "-store"

    @app.callback(Output(store, 'data'),
                  Input(store_name, 'value'),
                  State(store, 'data'))
    def on_click(new_val, stored_val):
        if new_val == stored_val["value"]:
            raise PreventUpdate

        data = {'value': new_val}
        return data


@app.callback(
    Output('placeholder4', 'children'),
    Input('table-editing-simple', 'data'),
    Input('table-editing-simple', 'columns'))
def table_manually_updated(rows, columns):
    # get the events from the table, reverse the order of the rows
    table_events = pd.DataFrame(rows, columns=[c['name'] for c in columns])[::-1]
    # import same number of events, that are supposed to be in the table, from disk
    disk_table_events = pd.read_csv("Baby_Events.csv")[::-1].iloc[0:events_to_display]

    # If table_events had a row deleted
    if len(table_events) < len(disk_table_events):
        # find the row that was deleted
        concat_rows = pd.concat([disk_table_events, table_events])
        deleted_row = concat_rows[~concat_rows.duplicated(keep=False)]
        # import all events from disk
        all_events_plus_deleted = pd.concat([pd.read_csv("Baby_Events.csv"), deleted_row])
        all_events_plus_deleted[~all_events_plus_deleted.duplicated(keep=False)].to_csv("Baby_Events.csv", index=False)

    else:  # the two tables are the same size, so an edit was made
        # import all events from disk
        all_events = pd.read_csv("Baby_Events.csv")
        update_all_event = pd.concat([all_events.iloc[:(len(all_events) - len(table_events))], table_events],
                                     ignore_index=True)
        update_all_event.to_csv("Baby_Events.csv", index=False)

    return ''


if __name__ == '__main__':
    app.run_server(debug=False, host="0.0.0.0")
