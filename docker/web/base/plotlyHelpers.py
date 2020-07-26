import plotly
import numpy as numpy


def multiple_line(df, column_x, columns_y, title=None, title_y=None):
    layout = plotly.graph_objs.Layout(
        title=title,
        xaxis={'title': column_x},
        yaxis=dict(title=title_y),
    )
    data = []
    for column in columns_y:
        data.append(plotly.graph_objs.Scatter(
            x=df[column_x], y=df[column], marker={'symbol': 104, 'size': 5}, mode="lines", name=column))
    figure = plotly.graph_objs.Figure(data=data, layout=layout)
    div = plotly.offline.plot(figure, auto_open=False, output_type='div', include_plotlyjs=False)
    return div


def double_line(df, column1, column2, column_x, title1=None, title2=None, title_x=None, dual_y_axis=True, title=None):
    if title1 is None:
        title1 = column1
    if title2 is None:
        title2 = column2
    if title_x is None:
        title_x = column_x
    if title is None:
        title = title1 + ' and ' + title2 + ' trending'
    y_data = df[column1]
    y_data2 = df[column2]
    x_data = df[column_x]
    trace1 = plotly.graph_objs.Scatter(x=x_data, y=y_data, marker={'color': 'red', 'symbol': 104, 'size': 5},
                                       mode="lines", name=title1)
    if dual_y_axis:
        trace2 = plotly.graph_objs.Scatter(x=x_data, y=y_data2, marker={'color': 'blue', 'symbol': 104, 'size': 5},
                                           mode="lines", name=title2, yaxis='y2')
    else:
        trace2 = plotly.graph_objs.Scatter(x=x_data, y=y_data2, marker={'color': 'blue', 'symbol': 104, 'size': 5},
                                           mode="lines", name=title2)
    layout = plotly.graph_objs.Layout(
        title=title,
        xaxis={'title': title_x},
        yaxis=dict(title=title1),
    )
    if dual_y_axis:
        layout.yaxis2 = dict(title=title2, overlaying='y', side='right')
    data = [trace1, trace2]
    figure = plotly.graph_objs.Figure(data=data, layout=layout)
    div = plotly.offline.plot(figure, auto_open=False, output_type='div', include_plotlyjs=False)
    return div


def single_line(df, column_x, column_y, title_x=None, title_y=None, title=None):
    if title_x is None:
        title_x = column_x
    if title_y is None:
        title_y = column_y
    if title is None:
        title = f'{title_x} versus {title_y}'
    x_data = df[column_x]
    y_data = df[column_y]
    trace1 = plotly.graph_objs.Scatter(x=x_data, y=y_data, marker={'color': 'blue', 'symbol': 104, 'size': 5},
                                       mode="lines", name=title_y)
    layout = plotly.graph_objs.Layout(
        title=title,
        xaxis={'title': title_x},
        yaxis=dict(title=title_y),
    )
    figure = plotly.graph_objs.Figure(data=[trace1], layout=layout)
    div = plotly.offline.plot(figure, auto_open=False, output_type='div', include_plotlyjs=False)
    return div


def double_bar_breakout(df, breakout, bar1, bar2, is_per_spot):
    df_breakout = df.groupby(breakout).agg(
        {bar1: numpy.sum, bar2: numpy.sum, 'spots': numpy.sum})
    df_breakout['zero'] = 0
    y1 = df_breakout[bar1].astype('float64')
    y2 = df_breakout[bar2].astype('float64')
    if is_per_spot:
        y1 = y1 / df_breakout.spots.astype('float64')
        y2 = y2 / df_breakout.spots.astype('float64')
    bars1 = plotly.graph_objs.Bar(x=df_breakout.index, y=y1, name=bar1)
    bars2 = plotly.graph_objs.Bar(x=df_breakout.index, y=y2, yaxis='y2', name=bar2)
    # see hack for grouped bar with secondary axis: https://github.com/plotly/plotly.js/issues/78
    hackbar1 = plotly.graph_objs.Bar(x=df_breakout.index, y=df_breakout.zero, hoverinfo='none', showlegend=False)
    hackbar2 = plotly.graph_objs.Bar(x=df_breakout.index, y=df_breakout.zero, hoverinfo='none', showlegend=False,
                                     yaxis='y2')
    layout = plotly.graph_objs.Layout(
        barmode='group',
        title=bar1 + ' and ' + bar2 + ' breakout by ' + breakout,
        xaxis={'title': breakout},
        yaxis=dict(title=bar1),
        yaxis2=dict(title=bar2, overlaying='y', side='right')
    )
    figure = plotly.graph_objs.Figure(data=[bars1, hackbar1, hackbar2, bars2], layout=layout)
    div = plotly.offline.plot(figure, auto_open=False, output_type='div', include_plotlyjs=False)
    return div
