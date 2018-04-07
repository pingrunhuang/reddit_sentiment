import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Event, Output, Input
import plotly.graph_objs as go
import pandas as pd
from DBUtil import database
from cache import cache

MAX_RECENT_POSTS = 10

app_colors = {
    "text": "#0C0F0A",
    "background": "#ffffff"
}

app = dash.Dash(__name__)

app.layout = html.Div([
        html.Div(
            className="container-fluid",
            children=[
                html.H1("Live reddit sentiment"),
                html.H5("Search:"),
                dcc.Input(id="keyword", type="text", value="")
            ], style={'width':'50%','margin-left':10,'margin-right':60,'max-width':50000}
        ),
        
        html.Div(className="row", children=[
            html.Div(id="recent-reddit-table", className="col s12 m6 l6"),
            html.Div(dcc.Graph(id="sentiment-pie", animate=False), className="col s12 m6 l6")
        ]),

        dcc.Interval(
            id="recent-reddit-table-update",
            interval=5*1000
        ),

        dcc.Interval(
            id="sentiment-pie-update",
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
                    style={"color":app_colors["text"]}
                )
            ),
            html.Tbody(
                [html.Tr(children=[
                    html.Td(data) for data in row 
                ], style={"color":app_colors["text"]}
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
    df = database.get_recent_reddit(sentiment_term)
    update_pos_neg_neutral_cache(sentiment_term, df)
    return generate_table(df)

@app.callback(
    Output("sentiment-pie", "figure"),
    [Input("keyword", "value")],
    events=[Event("sentiment-pie-update", "interval")]
)
def update_sentiment_pie(sentiment_term):
    # get data from cache
    # for i in range(100):
    #     sentiment_pie_dict = {}cache.get("")
    #     if sentiment_pie_dict:
    #         break
    #     time.sleep(0.1)
    # sentiment_pie_dict = [99,2]

    # if not sentiment_pie_dict:
    #     return None
    if sentiment_term=="":
        sentiment_term = "all"
    labels = ['Positive','Negative']
    try:
        pos = int(cache.get("positive_count").decode("utf8"))
        neg = int(cache.get("negative_count").decode("utf8"))
        neu = int(cache.get("neutral_count").decode("utf8"))
    except AttributeError:
        # the cache is not initialized yet
        historical_df = database.get_recent_reddit(sentiment_term, num=100000)
        pos, neg, neu = update_pos_neg_neutral_cache(sentiment_term, historical_df)
        del historical_df
    values = [pos,neg]
    colors = ['#007F25', '#800000']

    # the hoverinfo is shown when you hover on the chart
    # the textinfo is shown on the chart when not hovered
    trace = go.Pie(labels=labels,values=values,hoverinfo="label+percent",textinfo="value")

    return {"data":[trace],
            'layout':go.Layout(
                    title='Positive vs Negative sentiment for "{}" (longer-term)'.format(sentiment_term),
                    showlegend=True
                    )
            }



def quick_color(s):
    # except return bg as app_colors['background']
    if s >= POS_NEG_NEUT:
        # positive
        return "#002C0D"
    elif s <= -POS_NEG_NEUT:
        # negative:
        return "#270000"
    else:
        return app_colors['background']

def update_pos_neg_neutral_cache(sentiment_term, df):
    """
    This method is used for updating positive, negative and neutral counts when reddit streaming comes in
    df is only the incremented part of the sentiment table
    """
    THRESHOLD=0.3
    pos = len(list([x for x in df["sentiment"] if float(x)>=THRESHOLD]))
    neg = len(list([x for x in df["sentiment"] if float(x)<=-THRESHOLD]))
    neutral = len(list([x for x in df["sentiment"] if float(x)<THRESHOLD and float(x)>-THRESHOLD]))
    old_pos = cache.get("positive_count_{}".format(sentiment_term))
    old_neg = cache.get("negative_count_{}".format(sentiment_term))
    old_neu = cache.get("neutral_count_{}".format(sentiment_term))
    if old_pos:
        cache.client.incr("positive_count_{}".format(sentiment_term), pos)
    else:
        cache.set("positive_count_{}".format(sentiment_term), pos)
    
    if old_neg:
        cache.client.incr("negative_count_{}".format(sentiment_term), neg)
    else:
        cache.set("negative_count_{}".format(sentiment_term), neg)
    
    if old_neu:
        cache.client.incr("neutral_count_{}".format(sentiment_term), neutral)
    else:
        cache.set("neutral_count_{}".format(sentiment_term), neutral)
    return (pos, neg, neutral)




external_css = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"]
for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
for js in external_js:
    app.scripts.append_script({'external_url': js})


if __name__ == "__main__":
    app.run_server(debug=True)



