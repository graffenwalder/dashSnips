import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from pandas_datareader import data, wb
from datetime import date

tick = 'AAPL'
start = '2017-01-01'
end = date.today()

tick = tick.upper()
df = data.DataReader(tick, 'iex', start, end)

app = dash.Dash()
app.title=f'RSI: {tick}'

app.layout = html.Div([
            html.Div([
            dcc.Graph(id='rsi_main',
                    relayoutData = {'xaxis.range[0]': start,
                                    'xaxis.range[1]': end}),
            dcc.Graph(id='rsi_graph',
                    relayoutData = {'xaxis.range[0]': start,
                                    'xaxis.range[1]': end}),
            ],id='rsi_graphs_div'),

            html.Div([
                html.H4('RSI (period)'),
                dcc.Slider(id='slider_rsi',className='sliders',
                            min=5,
                            max=60,
                            step=1,
                            marks={i: f'{i}' for i in range(5,65,5)},
                            value=14)
            ],id='slider_rsi_div',className='slid_divs'),

],id='moad')
app.css.append_css({'external_url': 'http://memakewebsite.com/css/newstyle.css'})

# Main Graph
@app.callback(Output('rsi_main','figure'),
            [Input('rsi_graph', 'relayoutData')])
def update_main(r_relay):
    data = [go.Scatter(x=df.index,y=df['close'],name=f'{tick} RSI')]

    if 'xaxis.range[0]' in r_relay:
        layout = go.Layout(title= f'RSI: {tick}',
                autosize=False,height=400,
                margin=go.layout.Margin(l=45,r=10,b=23,t=70,pad=4),
                xaxis=dict(
                    autorange=False,
                    range= [r_relay['xaxis.range[0]'], r_relay['xaxis.range[1]']],
                    zeroline=False,
                    showline=False,
                    ticks='',
                    showticklabels=False))
    else:
        layout = go.Layout(title= f'RSI: {tick}',
                autosize=False,height=400,
                margin=go.layout.Margin(l=45,r=10,b=23,t=70,pad=4),
                xaxis=dict(
                    zeroline=False,
                    showline=False,
                    ticks='',
                    showticklabels=False))

    return {'data':data,'layout':layout}

#RSI Graph
@app.callback(Output('rsi_graph','figure'),
            [Input('slider_rsi','value'),
            Input('rsi_main', 'relayoutData')])
def update_rsi(rsi,m_relay):
    df['Up']=df['close'].diff().apply(lambda x:x if x>0 else 0)
    df['Down']=df['close'].diff().apply(lambda x:-x if x<0 else 0)
    df['UpAvg']=df['Up'].rolling(window=rsi).mean()
    df['DownAvg']=df['Down'].rolling(window=rsi).mean()
    df['RSI']=100-(100/(1+df['UpAvg']/df['DownAvg']))

    data = [go.Scatter(x=df.index,y=df['RSI'],name=f'{rsi} period RSI')]

    if 'xaxis.range[0]' in m_relay:
        layout = go.Layout(autosize=False,height=150,
                margin=go.layout.Margin(l=45,r=10,b=50,t=10,pad=4),
                xaxis=dict(
                    autorange=False,
                    range= [m_relay['xaxis.range[0]'], m_relay['xaxis.range[1]']],
                    ))
    else:
        layout = go.Layout(autosize=False,height=150,
                margin=go.layout.Margin(l=45,r=10,b=50,t=10,pad=4))

    return {'data':data,'layout':layout}

if __name__ == '__main__':
    app.run_server()
