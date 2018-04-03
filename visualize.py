
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Event, Output, Input
import plotly.graph_objs as go
import pandas as pd

MAX_RECENT_POSTS = 10

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div(
        children=[
            html.H1("Live reddit sentiment"),
            html.H5("Search:"),
            dcc.Input(id="keyword", type="text", value="reddit")
    ]
    ),
    
    html.Div(children=[
        html.Div(id="recent-reddit-table"),
        html.Div(dcc.Graph(id="sentiment-pie", animate=False))
    ]),

    dcc.Interval(
        id="recent-reddit-table-update",
        interval=60*1000
    )
]
)
def generate_table(df, max_rows=10):
    return html.Table(
        className="responsive-table", 
        children=[
            html.Thead(
                html.Tr(
                    children=[
                        html.Th(col.title()) for col in df.columns.values
                    ],
                    style={"color":colors["text"]}
                )
            ),
            html.Tbody(
                [html.Tr(children=[
                    html.Td(data) for data in row 
                ], style={"color":colors["text"]}
                ) for row in df.values.tolist()]
            )
        ]
        )


@app.callback(
    Output("recent-reddit-table", "children"),
    [Input("keyword", "value")],
    events=[Event("recent-reddit-table-update", "interval")]
)
def update_recent_reddit_table(sentiment_term):
    df = pd.DataFrame({"col1":[1,2,3,4,5,6], "col2":[1,2,3,4,5,6]})
    return generate_table(df)


if __name__ == "__main__":
    app.run_server(debug=True)



