import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

def graphing_line_2v (df, x, ym, ys):
    """ Graphing function for two axis

    :param df: Dataframe
    :type df: string
    :param x: Dataframe for axis x
    :type x: string
    :param ym: Dataframe for axis y primary
    :type ym: string
    :param ys: Dataframe for axis y secondary
    :type ys: string

    :returns: graph object
    :rtype: figure """

    xt =  df[x]
    yp = df[ym]
    yt = df[ys]
    # Making the graph for the two values
    fig_n = make_subplots(specs=[[{'secondary_y': True}]])
    fig_n.update_layout(title_text=ym + ' ' + ys + ' ' + 'Graph')
    fig_n.update_xaxes(title_text=x)
    fig_n.update_yaxes(title_text=ym, secondary_y=False)
    fig_n.update_yaxes(title_text=ys, secondary_y=True)
    fig_n.add_trace(go.Scatter(x=xt, y=yp, mode='lines', name=ym), secondary_y=False)
    fig_n.add_trace(go.Scatter(x=xt, y=yt, mode='lines', name=ys), secondary_y=True)
    return fig_n


def graphing_line_1v (df, x, y):
    """ Graphing function for one axis

    :param df: Dataframe
    :type df: string
    :param x: Dataframe for axis x
    :type x: string
    :param y: Dataframe for axis y primary
    :type y: string

    :returns: graph object
    :rtype: figure """

    xt =  df[x]
    yp = df[y]
    # Making the graph for the two values
    fig_n = make_subplots(specs=[[{'secondary_y': True}]])
    fig_n.update_layout(title_text=y + ' ' + 'Graph')
    fig_n.update_xaxes(title_text=x)
    fig_n.update_yaxes(title_text=y, secondary_y=False)
    fig_n.add_trace(go.Scatter(x=xt, y=yp, mode='lines', name=y), secondary_y=False)
    return fig_n



# bar_chart = px.bar(pivot_count_df, x='Profit', y='Sale', text='Sale',
#                    color_discrete_sequence=['#F63366']*len(pivot_df),
#                    template='plotly_white')
# st.plotly_chart(bar_chart)


def graphing_line_3v (df, x, ym, ys, yu):
    """ Graphing function for two axis

    :param df: Dataframe
    :type df: string
    :param x: Dataframe for axis x
    :type x: string
    :param ym: Dataframe for axis y primary
    :type ym: string
    :param ys: Dataframe for axis y secondary
    :type ys: string
    :param yu: Dataframe for axis y Third value
    :type yu: string

    :returns: graph object
    :rtype: figure """

    xt =  df[x]
    yp = df[ym]
    yt = df[ys]
    ytt = df[yu]
    # Making the graph for the two values
    fig_n = make_subplots(specs=[[{'secondary_y': True}]])
    fig_n.update_layout(title_text=ym + ' ' + ys + ' ' + yu + ' Graph')
    fig_n.update_xaxes(title_text=x)
    fig_n.update_yaxes(title_text=ym, secondary_y=False)
    fig_n.update_yaxes(title_text=ys, secondary_y=True)
    fig_n.update_yaxes(title_text=yu, secondary_y=False)
    fig_n.add_trace(go.Scatter(x=xt, y=yp, mode='lines', name=ym), secondary_y=False)
    fig_n.add_trace(go.Scatter(x=xt, y=yt, mode='lines', name=ys), secondary_y=True)
    fig_n.add_trace(go.Scatter(x=xt, y=ytt, mode='lines', name=yu), secondary_y=False)
    return fig_n


def graphing_line_4v (df, x, ym, ys, yu, yg):
    """ Graphing function for two axis

    :param df: Dataframe
    :type df: string
    :param x: Dataframe for axis x
    :type x: string
    :param ym: Dataframe for axis y primary
    :type ym: string
    :param ys: Dataframe for axis y secondary
    :type ys: string
    :param yu: Dataframe for axis y Third value
    :type yu: string

    :returns: graph object
    :rtype: figure """

    xt =  df[x]
    yp = df[ym]
    yt = df[ys]
    ytt = df[yu]
    yttt = df[yg]
    # Making the graph for the two values
    fig_n = make_subplots(specs=[[{'secondary_y': True}]])
    fig_n.update_layout(title_text=ym + ' ' + ys + ' ' + yu + ' Graph')
    fig_n.update_xaxes(title_text=x)
    fig_n.update_yaxes(title_text=ym, secondary_y=False)
    fig_n.update_yaxes(title_text=ys, secondary_y=True)
    fig_n.update_yaxes(title_text=yu, secondary_y=False)
    fig_n.update_yaxes(title_text=yg, secondary_y=True)
    fig_n.add_trace(go.Scatter(x=xt, y=yp, mode='lines', name=ym), secondary_y=False)
    fig_n.add_trace(go.Scatter(x=xt, y=yt, mode='lines', name=ys), secondary_y=True)
    fig_n.add_trace(go.Scatter(x=xt, y=ytt, mode='lines', name=yu), secondary_y=False)
    fig_n.add_trace(go.Scatter(x=xt, y=yttt, mode='lines', name=yg), secondary_y=True)
    return fig_n


### DID NOT WORK +++++TODO

# def graphing_line_xv (df, x, *args):
#     """ Graphing function for many axis

#     :param df: Dataframe
#     :type df: string
#     :param x: Dataframe for axis x
#     :type x: string
#     :param ym: Dataframe for axis y primary
#     :type ym: string

#     :returns: graph object
#     :rtype: figure """

#     xt =  df[x]
#     for elem in args:
#         fig_n.update_xaxes(title_text=x)
#         fig_n.update_yaxes(title_text=elem, secondary_y=False)
#         fig_n.add_trace(go.Scatter(x=xt, y=df[elem], mode='lines', name=elem), secondary_y=False)

#     return fig_n

